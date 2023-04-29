# Copyright 2020 Eugene Molotov <https://it-projects.info/team/em230418>
# License MIT (https://opensource.org/licenses/MIT).

from odoo import SUPERUSER_ID, models, _, exceptions, http
from odoo.http import request
import werkzeug
import logging
_logger = logging.getLogger(__name__)

class IrHttp(models.AbstractModel):
    _inherit = "ir.http"

    @classmethod
    def _dispatch(cls, endpoint):
        response = super()._dispatch(endpoint)
        database_suspend = request.env["ir.config_parameter"].sudo().get_param('database_suspend')
        path = '/database-blocked'

        exludes_path = [path, '/bus/websocket_worker_bundle']
        cur_user = request.env.user.id

        if database_suspend and request.httprequest.path not in exludes_path:
            if cur_user == 1:
                return response
            else:
                request.session.logout()
                return request.redirect(path)

        elif not database_suspend and request.httprequest.path == path:
            return request.redirect('/')
        else:
            return response
