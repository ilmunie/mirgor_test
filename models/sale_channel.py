from odoo import fields, models, _, api

class SaleChannel(models.Model):
    _name = 'sale.channel'
    _description = 'Sale Channel'

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)
    warehouse_id = fields.Many2one('stock.warehouse', string="Warehouse", required=True)
    journal_id = fields.Many2one('account.journal', string="Invoicing Journal", required=True, domain=[('type', '=', 'sale')])

    _sql_constraints = [
        ('code_unique', 'unique(code)', 'The code must be unique for each sales channel!')
    ]