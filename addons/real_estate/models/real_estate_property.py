from odoo.exceptions import UserError
from odoo import api, fields, models


class RealEstateProperty(models.Model):
    _name = 'real.estate.property'
    _description = 'New Model Description'
    _order = 'id desc'  # Default ordering
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='New Property ID',
        default='New',
        readonly=True,
        copy=False,
        tracking=True,
        index=True,
        sanitize=True,
        required=True,
    )
    code = fields.Char(string='ID Prefix')
    _unique_property_name = models.Constraint(
        'UNIQUE(name)',
        'Property ID must be unique',
    )
    salesperson_id = fields.Many2one(
        'res.users',
        string='Salesperson',
        default=lambda self: self.env.user,
        tracking=True,
    )
    buyer_id = fields.Many2one(
        'res.partner',
        string='Buyer',
    )
    discription = fields.Char(string='Description')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('rejected', 'Rejected'),
    ],

        string='Status',
        default='draft',
        required=True,
        copy=False,
        readonly=True,
        tracking=True,
    )
    offer = fields.Boolean(
        string='Offer',
    )
    reject = fields.Boolean(
        string='Reject',
    )
    property_type_id = fields.Many2one(
        'real.estate.types',
        string='Property Type',
        required=True,
        ondelete='cascade',
        tracking=True,
    )
    tags_id = fields.Many2many(
        'real.estate.tags',
        'property_id',
        'tag_id',
        string='Tags',
    )
    has_garden = fields.Boolean(
        compute='_compute_feature_flags',
    )
    has_grass = fields.Boolean(
        compute='_compute_feature_flags',
    )
    has_garage = fields.Boolean(
        compute='_compute_feature_flags',
    )
    has_gym = fields.Boolean(
        compute='_compute_feature_flags',
    )
    has_swimming_pool = fields.Boolean(
        compute='_compute_feature_flags',
    )
    garden_size = fields.Float(
        string='Garden Size'
    )
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        
        ('west', 'West'),
    ]
    )
    grass_size = fields.Float(
        string='Grass Field Size'
    )
    garage_size = fields.Float(
        string='Garage Size'
    )
    garage_capacity = fields.Integer(
        string='Vehicle Capacity'
    )
    gym_size = fields.Float(
        string='Gym Size'
    )
    pool_length = fields.Float(
        string='Pool Length'
    )
    pool_width = fields.Float(
        string='Pool Width'
    )
    pool_depth = fields.Float(
        string='Pool Depth'
    )
    postal_code = fields.Char(string='Post Code', required=True)
    bedrooms = fields.Integer(string='Bedrooms')
    living_areas = fields.Integer(
        string='Living Areas(sqm)',
        required=True,
    )
    available_from = fields.Datetime(string='Available From', required=True, readonly="state != 'draft'", )
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id,
    )
    expected_price = fields.Monetary(string='Expected Price', required=True, tracking=True)
    best_offer = fields.Monetary(
        string='Best Offer',
        readonly=True,
        tracking=True,
        compute= '_compute_best_offer',
        store=True,
    )
    selling_price = fields.Monetary(string='Selling Price', readonly=True, tracking=True)

    offer_ids = fields.One2many(
        'real.estate.offers',
        'property_id',
        string='Offer',
    )
    active = fields.Boolean(default=True)

    def action_confirm(self):
        for property_record in self:
            if property_record.state != 'draft':
                raise UserError(
                    'Only new property can be confirmed.'
                )
            else:
                property_record.state = 'confirmed'
        return True

    def action_reset_to_draft(self):
        for property_record in self:
            if (property_record.state != 'confirmed' or property_record.offer_ids):
                raise UserError('စောက်တောသားတေ Reset မရဘူးကွ ဟားဟားဟား')
            property_record.state = 'draft'
        return True

    @api.depends('tags_id', 'tags_id.code')
    def _compute_feature_flags(self):
        for property_record in self:
            selected_codes = set(
                property_record.tags_id.mapped('code')
            )
            property_record.has_garden = ('garden' in selected_codes)
            property_record.has_grass = ('grass' in selected_codes)
            property_record.has_garage = ('garage' in selected_codes)
            property_record.has_gym = ('gym' in selected_codes)
            property_record.has_swimming_pool = ('swimming_pool' in selected_codes)

    @api.model_create_multi
    def create(self, vals_list):
        sequence = self.env.ref(
            'real_estate.seq_real_estate_property',
            raise_if_not_found=False,
        )

        if not sequence:
            raise UserError(
                "Property sequence not found. "
                "Please check the sequence XML file and module name."
            )

        for values in vals_list:
            if values.get('name', 'New') != 'New':
                continue

            type_id = values.get('property_type_id')
            property_type = self.env[
                'real.estate.types'
            ].browse(type_id).exists() if type_id else False

            if not property_type or not property_type.code:
                raise UserError(
                    "Please select a Property Type with a valid code."
                )

            number = sequence.next_by_id()

            if not number:
                raise UserError(
                    "Unable to generate Property ID."
                )

            values['name'] = (
                f"{property_type.code.strip().upper()}/{number}"
            )

        return super().create(vals_list)
    @api.depends(
        'offer_ids',
        'offer_ids.price',
        'offer_ids.status',
    )
    def _compute_best_offer(self):
        for property_record in self:
            eligible_offer = property_record.offer_ids.filtered(
                lambda offer: offer.status in (
                    'pending','accepted',
                )
            )

            prices = eligible_offer.mapped('price')

            property_record.best_offer = max(prices, default=0.0)
