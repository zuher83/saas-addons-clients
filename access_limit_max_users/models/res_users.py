from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResUsers(models.Model):
    _inherit = "res.users"

    is_excluded_from_limiting = fields.Boolean(default=False, compute="_compute_is_excluded_from_limiting", store=True)

    @api.depends('active', 'groups_id')
    def _compute_is_excluded_from_limiting(self):
        for user in self:
            user_ids = ['base.default_user', 'base.template_portal_user_id', 'base.public_user', 'base.user_root']
            external_id = user.get_external_id()

            if external_id[user.id] in user_ids or not user.has_group('base.group_user') or (user.has_group('base.group_user') and user.active is False):
                user.is_excluded_from_limiting = True
            else:
                user.is_excluded_from_limiting = False

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("is_excluded_from_limiting") and not self.env.is_superuser():
                raise ValidationError(
                    _(
                        "Only superuser can create user with positive is_excluded_from_limiting value"
                    )
                )
            return super(ResUsers, self).create(vals_list)

    def write(self, vals):
        if vals.get("is_excluded_from_limiting") and not self.env.is_superuser():
            raise ValidationError(
                _(
                    "Only superuser can set user with positive is_excluded_from_limiting value"
                )
            )
        return super(ResUsers, self).write(vals)
