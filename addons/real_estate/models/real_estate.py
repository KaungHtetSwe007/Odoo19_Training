from odoo import api, fields, models
class RealEstate(models.Model):
    _name = 'real.estate'
    _description = 'New Model Description'
    _order = 'id desc'  # Default ordering

    title = fields.Char(string='Title', required=True)
    property_type = fields.Selection(
        [('house','House'),('apartment','Apartment')],
        string='Property Type',
        required=True
    )
    postal_code = fields.Char(string='Post Code', required=True)
    bedrooms = fields.Integer(string='Bedrooms')
    living_areas = fields.Integer(string='Living Areas(sqm)', required=True)
    available_from = fields.Datetime(string='Available From', required=True)
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id,
    )
    expected_price = fields.Monetary(string='Expected Price', required=True)
    best_offer = fields.Monetary(string='Best Offer')
    selling_price = fields.Monetary(string='Selling Price')
