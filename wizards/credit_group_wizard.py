from odoo import models, fields, api

class CreditGroupWizard(models.TransientModel):
    _name = 'credit.group.wizard'
    _description = 'Credit Group Wizard'

    credit_group_id = fields.Many2one('sale.credit.group', string="Credit Group", required=True)

    def action_print_report(self):
        self.ensure_one()
        partners = []
        for partner in self.credit_group_id.partner_ids:
            partners.append({
                'name': partner.name,
                'vat': partner.vat or "",
                'phone': partner.phone or "",
                'email': partner.email or "",
                'used_credit': partner.used_credit,
            })
        sale_orders = []
        sales = self.credit_group_id.partner_ids.get_uninvoiced_sales()
        for sale in sales:
            sale_orders.append(
                {
                    'name': sale.name,
                    'partner_name': sale.partner_id.name,
                    'date': sale.date_order,
                    'amount_total': sale.amount_total,
                    'currency': sale.currency_id.symbol,
                    'pending_to_invoice': sale.amount_total - sale.amount_invoiced
                }
            )
        invoices = []
        invs = self.credit_group_id.partner_ids.get_unpaid_invoices()
        for inv in invs:
            invoices.append(
                {
                    'name': inv.name,
                    'partner_name': inv.partner_id.name,
                    'date': inv.invoice_date,
                    'currency': inv.currency_id.symbol,
                    'amount_residual': inv.amount_residual,
                }
            )
        data = {'company_currency': self.env.user.company_id.currency_id.symbol,
                'name': self.credit_group_id.name,
                'code': self.credit_group_id.code,
                'channel': self.credit_group_id.sale_channel_id.name + " - " + self.credit_group_id.sale_channel_id.code,
                'global_credit': self.credit_group_id.global_credit,
                'used_credit': self.credit_group_id.used_credit,
                'available_credit': self.credit_group_id.available_credit,
                'partners': partners,
                'sale_orders': sale_orders,
                'invoices': invoices}
        return self.env.ref('mirgor_test.report_credit_group').report_action(self, data=data)
