from odoo import fields, models, _, api
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    sale_channel_id = fields.Many2one('sale.channel', string="Sale Channel", required=True, tracking=True)
    invoicing_journal_id = fields.Many2one('account.journal', string="Invoicing Journal", domain=[('type', '=', 'sale')])

    @api.onchange('sale_channel_id')
    def _onchange_channel_values(self):
        for record in self:
            if record.sale_channel_id:
                record.warehouse_id = record.sale_channel_id.warehouse_id.id
                record.invoicing_journal_id = record.sale_channel_id.journal_id.id

    def _prepare_invoice(self):
        res = super(SaleOrder, self)._prepare_invoice()
        res['journal_id'] = self.invoicing_journal_id.id if self.invoicing_journal_id else False
        res['sale_channel_id'] = self.sale_channel_id.id if self.sale_channel_id else False
        return res

    @api.depends('invoice_ids', 'invoice_ids.state')
    def _compute_amount_invoiced(self):
        for record in self:
            amount_inv = 0
            for posted_inv in record.invoice_ids.filtered(lambda x: x.state == 'posted'):
                amount_inv += posted_inv.currency_id._convert(posted_inv.amount_total, record.currency_id, posted_inv.company_id,
                                                posted_inv.invoice_date)
            record.amount_invoiced = amount_inv


    amount_invoiced = fields.Monetary(string='Amount Invoiced', compute=_compute_amount_invoiced, store=True)

    @api.depends('partner_id', 'partner_id.sale_credit_group_id', 'amount_total')
    def compute_credit_status(self):
        for record in self:
            res = 'no_limit'
            if record.partner_id and record.partner_id.sale_credit_group_id:
                if record.amount_total > record.partner_id.sale_credit_group_id.available_credit:
                    res = 'blocked_credit'
                else:
                    res = 'available_credit'
            record.credit_status = res


    credit_status = fields.Selection(selection=[('no_limit', 'No Credit Limit'),
                                               ('available_credit', 'Available Credit'),
                                               ('blocked_credit', 'Blocked Credit')], compute=compute_credit_status, store=True)

    @api.constrains("state", "amount_total")
    def _check_credit_status(self):
        for record in self:
            if record.state == 'sale' and record.credit_status == 'blocked_credit':
                msg = _("Can not confirm a sale order with no available credit!")
                raise ValidationError(msg)