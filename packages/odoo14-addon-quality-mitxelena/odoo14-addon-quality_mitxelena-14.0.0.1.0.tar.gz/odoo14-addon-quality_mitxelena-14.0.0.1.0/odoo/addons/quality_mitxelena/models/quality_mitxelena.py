from odoo import api, fields, models, _
from logging import getLogger
_logger = getLogger(__name__)

class Product(models.Model):
    _inherit = ["product.template"]
    product_test = fields.Many2one(comodel_name='qc.test', string='Test', tracking=True)
    test_question = fields.One2many(related='product_test.test_lines')