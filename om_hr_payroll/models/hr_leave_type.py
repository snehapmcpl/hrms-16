# -*- coding:utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import AccessError, UserError, ValidationError


class LeaveType(models.Model):
    _inherit = 'hr.leave.type'

    code = fields.Char(string='Code')
    documents_mandatory_days = fields.Integer(string="Documents should me mandatory,The days more than")


class Leave(models.Model):
    _inherit = 'hr.leave'

    documents_needed = fields.Boolean(string="Documents Needed?",default=False)

    @api.model
    def create(self, vals):
        result = super(Leave, self).create(vals)
        if vals.get('holiday_status_id'):
            if vals.get('number_of_days'):
                leave_type_obj = self.env['hr.leave.type'].search([('id', '=', vals.get('holiday_status_id'))])
                for leave_type in leave_type_obj:
                    if leave_type.support_document:
                        if vals.get('number_of_days') > leave_type.documents_mandatory_days:
                            if not result.supported_attachment_ids:
                                raise ValidationError('Please update the document for sick leave.')
        return result

    def write(self, vals):
        result = super(Leave, self).write(vals)
        for rec in self:
            if rec.holiday_status_id:
                for leave_type in rec.holiday_status_id:
                    if leave_type.support_document:
                        if rec.number_of_days > leave_type.documents_mandatory_days:
                            if not rec.supported_attachment_ids:
                                raise ValidationError('Please update the document for sick leave.')

        return result

