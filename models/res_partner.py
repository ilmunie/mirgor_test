from odoo import fields, models, _, api
from odoo.tools import float_round

class ResPartner(models.Model):
    _inherit = 'res.partner'

    credit_control = fields.Boolean(string="Credit Control")
    sale_channel_id = fields.Many2one(related='sale_credit_group_id.sale_channel_id')
    sale_credit_group_id = fields.Many2one('sale.credit.group', string="Sale Credit Group")
    used_credit = fields.Monetary(string="Used Credit", compute='_compute_used_credit', currency_field='currency_id', store=True)


    @api.depends('sale_order_ids.state',
                 'sale_order_ids.amount_total',
                 'sale_order_ids.invoice_ids.amount_residual',
                 'sale_order_ids.invoice_ids.state')
    def _compute_used_credit(self):
        for partner in self:
            total_uninvoiced_sales = partner._get_total_uninvoiced_sales()
            total_unpaid_invoices = partner._get_total_unpaid_invoices()
            partner.used_credit = float_round(total_uninvoiced_sales + total_unpaid_invoices, precision_digits=2)

    def get_uninvoiced_sales(self):
        sales_orders = self.env['sale.order'].search([
            ('partner_id', 'in', self.mapped('id')),
            ('state', 'in', ['sale', 'done']),
            ('invoice_status', '=', 'to invoice')
        ])
        return sales_orders

    def get_unpaid_invoices(self):
        invoices = self.env['account.move'].search([
            ('partner_id', 'in', self.mapped('id')),
            ('state', '=', 'posted'),
            ('payment_state', '!=', 'paid'),
            ('move_type', '=', 'out_invoice')
        ])
        return invoices

    def _get_total_uninvoiced_sales(self):
        self.ensure_one()
        sales_orders = self.get_uninvoiced_sales()
        total = 0.0
        for order in sales_orders:
            total += order.currency_id._convert(order.amount_total - order.amount_invoiced, self.currency_id, self.company_id,
                                                order.date_order)
        return total

    def _get_total_unpaid_invoices(self):
        self.ensure_one()
        invoices = self.get_unpaid_invoices()
        total = 0.0
        for invoice in invoices:
            total += invoice.currency_id._convert(invoice.amount_residual, self.currency_id, self.company_id,
                                                  invoice.invoice_date)
        return total
