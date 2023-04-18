# Copyright 2020 Eugene Molotov <https://it-projects.info/team/em230418>
# License MIT (https://opensource.org/licenses/MIT).

from odoo import SUPERUSER_ID, models, _, exceptions, http
from odoo.http import request
import werkzeug
import logging
_logger = logging.getLogger(__name__)

URL_REDIRECT = "www.google.com"


class IrHttp(models.AbstractModel):

    _inherit = "ir.http"

    def session_info(self):
        res = super(IrHttp, self).session_info()

        res["database_block_show_message_in_apps_menu"] = bool(
            self.env["ir.module.module"]
            .with_user(SUPERUSER_ID)
            .search(
                [("name", "=", "ey_theme_backend"), ("state", "=", "installed")], limit=1,
            )
        )
        database_suspend = self.env["ir.config_parameter"].sudo().get_param('database_suspend')

        if database_suspend == 'suspended':
            request.session.logout()
            request.redirect('/database-blocked')
        return res

    @classmethod
    def _dispatch(cls, endpoint):
        response = super()._dispatch(endpoint)
        database_suspend = request.env["ir.config_parameter"].sudo().get_param('database_suspend')
        path = '/database-blocked'

        exludes_path = [path, '/bus/websocket_worker_bundle']

        if database_suspend == "suspended" and request.httprequest.path not in exludes_path:
            return request.redirect(path)

        elif database_suspend != "suspended" and request.httprequest.path == path:
            return request.redirect('/')
        else:
            return response
