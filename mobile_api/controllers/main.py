from odoo import http
from odoo.http import request
import json
from odoo.exceptions import AccessDenied


class Service(http.Controller):

    @http.route('/app_authenticate', type='json', auth='public')
    def authenticate_app(self):
        print('app_authenticate')
        details = request.jsonrequest
        if not details.get('login') or not details.get('password'):
            return {'error': 'Login/Password is not set'}
        try:
            uid = request.session.authenticate(request.session.db, details['login'], details['password'])
        except AccessDenied as e:
            # request.uid = 10
            return {'status': 'Access denied!'}
        return {'status': 'Successfully logged in'}



    @http.route('/app_list_employees', type='json', auth='public')
    def get_employees(self):
        details = request.jsonrequest
        if not details.get('login') or not details.get('password'):
            return {'error': 'Login/Password is not set'}
        try:
            uid = request.session.authenticate(request.session.db, details['login'], details['password'])
        except AccessDenied as e:
            return {'status': 'Access denied!'}
        employees = request.env['hr.employee'].search([])
        employees_dict = list()
        for employee in employees:
            if employee.user_id.login == details.get('login'):
                employees_dict.append({
                    'id': employee.id,
                    'name': employee.name,
                    'job_title ' : employee.job_title,
                    'work_mobile' : employee.mobile_phone,
                    'work_email' : employee.work_email,
                    'work_phone' : employee.work_phone,
                    'department_name' : employee.department_id.name,
                    'manager_name' : employee.parent_id.name,
                    'pan' : employee.employee_pan_no,
                    'work_location': employee.work_location_id.name,
                    'father_name': employee.father_name_emp,
                    'father_dob': employee.father_dob,
                    'mother_name': employee.mother_name_emp,
                    'mother_dob': employee.mother_dob,
                    'spouse_name': employee.spouse_name_emp,
                    'spouse_dob': employee.spouse_dob,
                    'bank_acc_num':employee.bank_account_id.acc_number,
                    'joining_date':employee.date_join,
                    'nationality':employee.country_id.name,
                    'identification_num':employee.identification_id,
                    'passport_num':employee.passport_id,
                    'gender':employee.gender,
                    #'age':employee.age,
                    'marital_status':employee.marital,
                    'salary_info':employee.total_ctc,
                })
        return {'status': 'Successfully logged in', 'employees_list': employees_dict}















