#!/usr/bin/bash

set -eu -o pipefail

COLORS="lightblue salmon lightyellow lightgreen white"

function usage() {
    echo "usage: $0 [-h] [--force]"
    echo "optional arguments:"
    echo "  -h, --help   show this help message and exit"
    echo "  --force      enforce recreation of all images"
    echo "  --show       display the category images after creation"
    echo "  --clean      remove all generated images"
}

# NOTE: This requires GNU getopt.
ARGS=$(/usr/bin/getopt -o h --long help,clean,force,show -- "$@")
if [ $? != 0 ] ; then echo "Terminating..." >&2 ; exit 1 ; fi
eval set -- "$ARGS"

FORCE=
SHOW=
CLEAN=
while true; do
  case "$1" in
    -h | --help ) usage; exit ; shift ;;
    --force )
        FORCE=yes
        shift ;;
    --clean )
        CLEAN=yes
        shift ;;
    --show )
        SHOW=yes
        shift ;;
    -- ) shift ; break ;;
    * ) usage; exit 1 ; shift ;;
  esac
done

cd $(dirname "$0")

for type in T-Shirt Polo-Shirt ; do
    for color in $COLORS ; do
	for side in front back ; do
	    src=$type-blue-$side.svg
	    svg=$type-$color-$side.svg
	    png=${svg%.svg}.png

	    if [ -n "$FORCE" -o -n "$CLEAN" ] ; then
		rm $svg $png
	    fi
	    if [ -n "$CLEAN" ] ; then
		continue
	    fi
	    if [ ! -f $svg ] ; then
		echo creating $svg
		sed < $src > $svg -e 's/fill:#0000ff;/fill:'$color';/'
	    fi
	    if [ ! -f $png ] ; then
		echo creating $png
		convert -resize 800x800 $svg $png
	    fi
	done
    done
done

rm *-shirts*.png

if [ -z "$CLEAN" ] ; then
    magick montage T-Shirt-{light*,salmon}-front.png \
	   -geometry 200x200+2+2 -tile 2x2 t-shirts.png
    magick montage Polo-Shirt-{salmon,light*}-front.png \
	   -geometry 200x200+2+2 -tile 2x2 polo-shirts.png

    if [ -n "$SHOW" ] ; then
	ls *-shirts*.png
	display *-shirts*.png
    fi
fi
