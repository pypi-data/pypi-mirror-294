# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta


class Carrier(metaclass=PoolMeta):
    __name__ = "carrier"

    comment = fields.Text('Comment',
        help='Internal comments for this carrier')
    delivery_comment = fields.Char('Delivery comment',
        help='For display on the website, e.g. expected delivery time')
