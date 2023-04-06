from odoo import api, fields, models,_
from datetime import date , timedelta


class ResignationRequest(models.TransientModel):
    _name = 'resignation.request.wizard'
    _description = 'Resignation Request Wizard'

    employee_id = fields.Many2one('hr.employee', string="Employee",
                                  help='Name of the employee for whom the request is creating')
    date_of_resignation = fields.Date(string="Resignation Date", default=date.today(),
                                      help='Date on which the request is confirmed by the employee.')
    # reason = fields.Many2one('hr.departure.reason', string="Reason", required=True,
    #                          help='Specify reason for leaving the company')
    reason = fields.Text("Reason of Resignation")
    notice_period = fields.Integer(string="Notice Period (in Days)")


    # def default_get(self, fields_list):
    #     res = super(ResignationRequest,self).default_get(fields_list)
    #     active_id = self._context.get('active_id')
    #     print('active_id+++++++++++++',active_id)
    #     brw_id = self.env['hr.employee'].browse(int(active_id))
    #     if active_id:
    #         res['employee_id'] = brw_id
    #         res['date_of_resignation'] = fields.date.today()
    #     return res

    # def default_get(self, fields_list):
    #     res = super(ResignationRequest,self).default_get(fields_list)
    #     active_id = self._context.get('active_id')
    #     print('active_id+++++++++++++',active_id)
    #     brw_id = self.env['hr.employee'].browse(int(active_id))
    #     # emp_id = self.employee_id
    #     emp_category = brw_id.emp_category
    #     recs = self.env['notice.period.days'].search([('employee_category', '=', emp_category)])
    #     print('recs', recs)
    #     if active_id:
    #         res['employee_id'] = brw_id
    #         # res['date_of_resignation'] = fields.date.today()
    #         for rec in recs:
    #             if brw_id.total_ctc >= rec.ctc_from and brw_id.total_ctc <= rec.ctc_to:
    #                 res['notice_period'] = rec.employee_notice_days
    #     return res

    def submit_request(self):
        reg_id = self.env['hr.departure.reason'].search([('name', '=', 'Resigned')])
        struct = self.env['hr.payroll.structure'].search([('name', '=', 'Final Settlement')])
        # self.write({'structure': struct.id})
        res_obj = self.env['hr.resignation']
        emp_id = self.employee_id
        emp_category = emp_id.emp_category
        recs = self.env['notice.period.days'].search([('employee_category','=',emp_category)])
        for rec in recs:
            if emp_id.total_ctc >= rec.ctc_from and emp_id.total_ctc <= rec.ctc_to:
                self.notice_period = rec.employee_notice_days
        # if self.date_of_resignation:
        #     self.date_of_relieving = ((self.date_of_resignation) + timedelta(days=self.notice_period))
        res_obj.create({'employee_id': emp_id.id,
                        'date_of_resignation': self.date_of_resignation,
                        'resignation_type': reg_id.id,
                        'notice_period': rec.employee_notice_days,
                        'date_of_relieving': ((self.date_of_resignation) + timedelta(days=self.notice_period)),
                        'reason': self.reason,
                        'structure': struct.id,
                        'state': 'discussion'})
