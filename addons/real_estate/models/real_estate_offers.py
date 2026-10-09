from datetime import timedelta
from odoo import fields, models, api
class RealEstateDescription(models.Model):
    _name = 'real.estate.offers'
    _description = 'New Model Offers'
    _order = 'id desc'  # Default ordering
    _inherit = [
        'mail.thread',
        'mail.activity.mixin',
    ]
    name = fields.Char(string='Offer ID', required=True,tracking=True)
    property_id = fields.Many2one(
        'real.estate.property',
        string='Property',
        tracking=True,
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Partner',
        required=True,
        ondelete='restrict',
        index=True,
    )
    price = fields.Monetary(
        string='Price',
        tracking=True,
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
    )
    validity = fields.Integer(
        string='Validity(days)',
        default=7,
        help= 'Number of days until expiration',
    )
    date_deadline = fields.Date(
        string='Date of Deadline',
        compute='_compute_date_deadline',
        inverse='_inverse_date_deadline',
        store=True,
    )
    status = fields.Selection(
        [
         ('pending','Pending'),
         ('accepted','Accepted'),
         ('rejected','Rejected'),
         ],
        string='Status',
        default='pending',
        required=True,
        copy=False,
    )
    note = fields.Text(
        string='Note',
    )
    _check_positive_price = models.Constraint(
        'CHECK(price > 0)',
        'The offer price must be greater than zero.',
    )

    _check_validity = models.Constraint(
        'CHECK(validity >= 0)',
        'The validity cannot be negative.',
    )

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for offer in self:
            start_date = (
                offer.create_date.date()
                if offer.create_date
                else fields.Date.context_today(offer)
            )

            offer.date_deadline = start_date + timedelta(
                days=offer.validity
            )

    def _inverse_date_deadline(self):
        for offer in self:
            if not offer.date_deadline:
                continue

            start_date = (
                offer.create_date.date()
                if offer.create_date
                else fields.Date.context_today(offer)
            )

            offer.validity = (
                    offer.date_deadline - start_date
            ).days