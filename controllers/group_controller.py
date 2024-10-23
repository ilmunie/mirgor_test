from odoo import http
from odoo.http import request


class CreditGroupController(http.Controller):

    @http.route('/api/credit_group', type='json', auth='public', methods=['POST'], csrf=False)
    def create_or_update_credit_group(self, **kwargs):
        data = http.request.jsonrequest
        response = {}
        request_data = data.get('grupo_creditos', [])
        if not request_data:
            response = {'status': '400', 'message': "Wrong Request Format. Please send 'grupo_creditos' as a key with list values"}
            return response
        for group in request_data:
            code = group.get('codigo')
            name = group.get('name')
            sale_channel_code = group.get('canal')
            global_credit = group.get('credito_global')

            sale_channel = request.env['sale.channel'].sudo().search([('code', '=', sale_channel_code)], limit=1)
            if not sale_channel:
                response[code] = {
                    'status': 400,
                    'message': f'Sale channel with code {sale_channel_code} does not exist.'
                }
                continue

            credit_group = request.env['sale.credit.group'].sudo().search([('code', '=', code)], limit=1)
            if credit_group:
                credit_group.sudo().write({
                    'name': name,
                    'sale_channel_id': sale_channel.id,
                    'global_credit': global_credit
                })
                response[code] = {'status': '200', 'message': "OK, Updated"}
            else:
                request.env['sale.credit.group'].sudo().create({
                    'name': name,
                    'code': code,
                    'sale_channel_id': sale_channel.id,
                    'global_credit': global_credit
                })
                response[code] = {'status': '200', 'message': "OK, Created"}
        return response