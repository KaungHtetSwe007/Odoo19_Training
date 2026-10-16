from odoo import api, fields, models
class RealEstateTags(models.Model):
    _name = 'real.estate.tags'
    _description = 'New Model Description'
    _order = 'id desc'  # Default ordering

    name = fields.Char(string='Tags', required=True)
    code = fields.Selection(
        [
            ('garden', 'Garden'),
            ('garage', 'Garage'),
            ('gym', 'Gym'),
            ('swimming_pool', 'Swimming Pool'),
            ('grass', 'Grass'),
            ('other', 'Other'),
        ]
    )
    color = fields.Integer(string='Color', required=True)
    _unique_name = models.Constraint(
        'UNIQUE(name)',
        'The property tag must be unique.',
    )