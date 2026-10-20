from datetime import timedelta
from odoo import fields, models, api
from odoo.exceptions import UserError


class RealEstateDescription(models.Model):
    _name = 'real.estate.offers'
    _description = 'New Model Offers'
    _order = 'id desc'  # Default ordering
    _inherit = [
        'mail.thread',
        'mail.activity.mixin',
    ]
    name = fields.Char(
        string='Offer ID',
        default= 'New',
        required=True,
        tracking=True,
        readonly= True,
        copy=False
    )
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
         ('expired', 'Expired'),
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

    @api.onchange('property_id')
    def _onchange_property_id(self):
        """Use the selected property's currency for this offer in the form."""
        if self.property_id:
            self.currency_id = self.property_id.currency_id
        else:
            self.currency_id = self.env.company.currency_id

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

    def action_accept(self):
        for offer in self:
            if offer.status != 'pending':
                raise UserError(
                    'Only pending offers can accept.'
                )
            today = fields.Date.context_today(offer)
            if offer.date_deadline and offer.date_deadline < today:
                raise UserError(
                    'Only pending offers can accept.'
                )
            accepted_offer = self.env['real.estate.offers'].search(
                [
                    ('property_id', '=', offer.property_id.id),
                    ('status', '=', 'accepted'),
                ], limit=1
            )
            if accepted_offer:
                raise UserError(
                    'Only pending offers can accept.'
                )
            if offer.property_id.state not in(
                'confirmed', 'offer_received'
            ):
                raise UserError('Only pending offers can accept.')
            other_pending_offer = self.env['real.estate.offers'].search(
                [
                    ('property_id', '=', offer.property_id.id),
                    ('status', '=', 'pending'),
                    ('id', '!=', offer.id),
                ]
            )
            other_pending_offer.write({
                'status': 'rejected',
            })
            offer.status = 'accepted'
            offer.property_id.write({
                'buyer_id': offer.partner_id.id,
                'selling_price': offer.price,
                'state' : 'offer_accepted'
            })
        return True
    def action_reject(self):
        for offer in self:
            if offer.status != 'pending':
                raise UserError('Only pending offers can reject.')

            offer.status = 'rejected'
            offer.property_id.write({
                'state' : 'rejected'
            })
        return True
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
           if vals.get('name', 'New') == 'New':
                vals['name'] = (
                    self.env['ir.sequence'].next_by_code('real.estate.offer') or 'New'
                )
        return super().create(vals_list)
    @api.model
    def _corn_expire_pending_offers(self):
        today = fields.Date.context_today(self)
        expired_offers = self.env['real.estate.offers'].search(
            [
                ('status', '=' ,'pending'),
                ('date_deadline', '<', today),

            ]
        )
        expired_offers.write({
            'status': 'expired',
        })
        return True
