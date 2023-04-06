# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from random import randint

from odoo import api, fields, models, tools, SUPERUSER_ID
from odoo.tools.translate import _
from odoo.exceptions import UserError, ValidationError


class Applicant(models.Model):
    _inherit = "hr.applicant"

    def create_employee_from_applicant(self):
        """ Create an hr.employee from the hr.applicants """
        employee = False
        for applicant in self:
            contact_name = False
            applicant_obj = self.env['hr.applicant'].search(
                [('job_id', '=', applicant.job_id.id)])
            applicant_list = []
            for app in applicant_obj:
                if app.emp_id:
                    applicant_list.append(app)
            applicant_len = len(applicant_list)
            if applicant.job_id.no_of_recruitment < applicant_len:
                raise ValidationError(_("Recruitment for this job position is already filled."))
            else:
                if applicant.partner_id:
                    address_id = applicant.partner_id.address_get(['contact'])['contact']
                    contact_name = applicant.partner_id.display_name
                else:
                    if not applicant.partner_name:
                        raise UserError(_('You must define a Contact Name for this applicant.'))
                    new_partner_id = self.env['res.partner'].create({
                        'is_company': False,
                        'type': 'private',
                        'name': applicant.partner_name,
                        'email': applicant.email_from,
                        'phone': applicant.partner_phone,
                        'mobile': applicant.partner_mobile
                    })
                    applicant.partner_id = new_partner_id
                    address_id = new_partner_id.address_get(['contact'])['contact']
                if applicant.partner_name or contact_name:
                    employee_data = {
                        'default_name': applicant.partner_name or contact_name,
                        'default_job_id': applicant.job_id.id,
                        'default_job_title': applicant.job_id.name,
                        'default_address_home_id': address_id,
                        'default_department_id': applicant.department_id.id or False,
                        'default_address_id': applicant.company_id and applicant.company_id.partner_id
                                              and applicant.company_id.partner_id.id or False,
                        'default_work_email': applicant.department_id and applicant.department_id.company_id
                                              and applicant.department_id.company_id.email or False,
                        'default_work_phone': applicant.department_id.company_id.phone,
                        'form_view_initial_mode': 'edit',
                        'default_applicant_id': applicant.ids,
                    }

            dict_act_window = self.env['ir.actions.act_window']._for_xml_id('hr.open_view_employee_list')
            dict_act_window['context'] = employee_data
            return dict_act_window
