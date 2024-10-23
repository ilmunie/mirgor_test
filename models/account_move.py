from odoo import fields, models, _, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    sale_channel_id = fields.Many2one('sale.channel', string="Sale Channel")

