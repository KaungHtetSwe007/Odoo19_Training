from odoo import fields, models
class RealEstateTypes(models.Model):
    _name = 'real.estate.types'
    _description = 'New Model Description'
    _order = 'id desc'  # Default ordering

    name = fields.Char(string='Property Type', required=True)
    property_id = fields.Many2one(
        'real.estate.property',
        string='Property',
    )
    active = fields.Boolean(default=True)
    _unique_name = models.Constraint(
        'UNIQUE(name)',
        'The property type must be unique.',
    )