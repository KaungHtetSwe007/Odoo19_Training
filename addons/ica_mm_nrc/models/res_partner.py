from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    state_code = fields.Char(string='State Code', related='state_id.code')
    township_id = fields.Many2one('res.country.state.township')
    township_code = fields.Char(string='Township Code', related='township_id.code')
    nrc_number = fields.Char(string="NRC Number")
