from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    if not version:
        return

    env = api.Environment(cr, SUPERUSER_ID, {})
    users = env['res.users'].search([])
    for user in users:
        user._compute_is_excluded_from_limiting()
