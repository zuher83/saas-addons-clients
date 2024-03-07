import odoo
from odoo import http
from odoo.http import request
from odoo.service import security
from odoo.addons.web.controllers.home import Home, ensure_db

class DatabaseSuspend(Home):

    @http.route()
    def web_client(self, s_action=None, **kw):
        ensure_db()
        response = super().web_client(s_action, **kw)
        database_suspend = request.env["ir.config_parameter"].sudo().get_param('database_suspend')

        if database_suspend and request.env.user.id != 1:
            return request.redirect('/database-blocked')
        else:
            return response

    @http.route('/web/become', type='http', auth='user', sitemap=False)
    def switch_to_admin(self):
        uid = request.env.user.id
        if request.env.user.id != 1:
            return request.redirect('/')

        if request.env.user._is_system():
            uid = request.session.uid = odoo.SUPERUSER_ID
            # invalidate session token cache as we've changed the uid
            request.env['res.users'].clear_caches()
            request.session.session_token = security.compute_session_token(request.session, request.env)

        return request.redirect(self._login_redirect(uid))

    @http.route('/database-blocked', type="http", website=True, auth='public')
    def database_blocked_page(self, **kw):
        return request.render("database_block.database-blocked")
