import odoo
from odoo import http
from odoo.http import request

from odoo.addons.website.controllers.main import Website


class DatabaseSuspend(Website):

    @http.route('/', type='http', auth="public", website=True, sitemap=True)
    def index(self, **kw):
        response = super().index(**kw)
        database_suspend = request.env["ir.config_parameter"].sudo().get_param('database_suspend')

        if database_suspend and request.env.user.id != 1:
            return request.redirect('/database-blocked')
        else:
            return response
