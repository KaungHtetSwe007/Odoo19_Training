from odoo import fields, models
class RealEstateDescription(models.Model):
    _name = 'real.estate.description'
    _description = 'New Model Description'
    _order = 'id desc'  # Default ordering

    description = fields.Char(string='Description', required=True)