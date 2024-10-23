from odoo import fields, models, _, api

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    sale_channel_id = fields.Many2one(related="sale_id.sale_channel_id", string="Sale Channel", store=True)
