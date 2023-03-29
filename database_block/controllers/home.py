from odoo import http
from odoo.http import request

class DatabaseSuspend(http.Controller):

    @http.route('/database-blocked', type="http", website=True, auth='public')
    def database_blocked_page(self, **kw):
        return request.render("database_block.database-blocked")
