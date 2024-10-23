from odoo import models, fields, api, _
from odoo.tools import float_round


class SaleCreditGroup(models.Model):
    _name = 'sale.credit.group'
    _description = 'Credit Group'


    name = fields.Char(string="Group Name", required=True)
    code = fields.Char(string="Group Code", required=True)

    _sql_constraints = [
        ('code_unique', 'unique(code)', 'The code must be unique for each sales channel!')
    ]
    sale_channel_id = fields.Many2one('sale.channel', string="Sales Channel", required=True)
    global_credit = fields.Monetary(string="Global Credit", required=True, currency_field='company_currency_id')
    company_currency_id = fields.Many2one('res.currency', string='Currency', related='company_id.currency_id', readonly=True, store=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)

    def view_partners(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Customers',
            'res_model': 'res.partner',
            'view_mode': 'tree,form',
            'view_ids': [('mirgor_test.view_partner_credit_tree', 'list'), (False, 'form')],
            'domain': [('sale_credit_group_id', '=', self.id)],
        }

    partner_ids = fields.One2many('res.partner', 'sale_credit_group_id')
    used_credit = fields.Monetary(string="Used Credit", compute='_compute_used_credit', currency_field='company_currency_id', store=True)
    available_credit = fields.Monetary(string="Available Credit", compute='_compute_available_credit', currency_field='company_currency_id', store=True)

    @api.depends('global_credit', 'used_credit')
    def _compute_available_credit(self):
        for group in self:
            group.available_credit = group.global_credit - group.used_credit

    @api.depends('partner_ids', 'partner_ids.used_credit')
    def _compute_used_credit(self):
        for group in self:
            group.used_credit = float_round(sum(group.partner_ids.mapped('used_credit')), precision_digits=2)

