# -*- coding: utf-8 -*-
from . import models
from . import wizards
from . import controllers
from odoo.service import common
from odoo.exceptions import UserError
from odoo import _

def pre_init_check(cr):
    version_info = common.exp_version()
    server_serie = version_info.get('server_serie')
    if server_serie != '15.0':
        raise UserError(_('Module Odoo Version 15.0 only and found ' + server_serie))
    return True