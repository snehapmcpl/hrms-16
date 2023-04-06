from odoo import models, fields, _, api


class GrossLines(models.Model):
    _inherit = 'res.company'

    # fiscal_year_last_month = fields.Selection([('1', 'January'),
    #                                            ('2', 'February'),
    #                                            ('3', 'March'),
    #                                            ('4', 'April'),
    #                                            ('5', 'May'),
    #                                            ('6', 'June'),
    #                                            ('7', 'July'),
    #                                            ('8', 'August'),
    #                                            ('9', 'September'),
    #                                            ('10', 'October'),
    #                                            ('11', 'November'),
    #                                            ('12', 'December')], string='Last Month')
    fiscal_year_last_date = fields.Date("End Date")
    fiscal_year_start_date = fields.Date("Start Date")
    tan_no = fields.Char("TAN")
    pan_no = fields.Char("PAN")
