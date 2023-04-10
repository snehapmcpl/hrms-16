import datetime

from odoo import fields
from odoo.http import db_monodb, request, root
from odoo.service import security

from odoo.addons.base_rest import restapi
from odoo.addons.component.core import Component
import logging


_logger = logging.getLogger(__name__)



def _rotate_session(httprequest):
    if httprequest.session.rotate:
        root.session_store.delete(httprequest.session)
        httprequest.session.sid = root.session_store.generate_key()
        if httprequest.session.uid:
            httprequest.session.session_token = security.compute_session_token(
                httprequest.session, request.env
            )
        httprequest.session.modified = True

class PartnerNewApiService(Component):
    _inherit = "base.rest.service"
    _name = "partner.new_api.service"
    _usage = "partner"
    _collection = "base_rest_auth_user_service.services"
    _description = """
        Partner New API Services
        Services developed with the new api provided by base_rest
    """

    @restapi.method(
        [(["/get_employee_details", "/"], "GET")],

        auth="user",
    )
    def get_employee_details(self):
        user_id = self.env.user
        employee = self.env['hr.employee'].search([('user_id', '=', user_id.id)])
        employees_dict = list()
        if employee:
            employees_dict.append({
                'id': employee.id,
                'name': employee.name,
                'job_title ': employee.job_title,
                'work_mobile': employee.mobile_phone,
                'work_email': employee.work_email,
                'work_phone': employee.work_phone,
                'department_name': employee.department_id.name,
                'manager_name': employee.parent_id.name,
                'pan': employee.employee_pan_no,
                'work_location': employee.work_location_id.name,
                'bank_acc_num': employee.bank_account_id.acc_number,
                'joining_date': employee.date_join,
                'nationality': employee.country_id.name,
                'identification_num': employee.identification_id,
                'passport_num': employee.passport_id,
                'gender': employee.gender,
                'age': employee.age,
                'marital_status': employee.marital,
                'salary_info': employee.total_ctc,
            })
            return {'status': 'Successfully logged in', 'employees_list': employees_dict}

    @restapi.method(
        [(["/get_dashboard_details", "/"], "GET")],

        auth="user",
    )
    def get_dashboard_details(self):
        print('get_dashboard_details++++++')
        user_id = self.env.user
        employee = self.env['hr.employee'].search([('user_id', '=', user_id.id)])
        employees_dict = list()
        if employee:
            print('str(employee.image_1920)',str(employee.image_1920))
            employees_dict.append({
                'id': employee.id,
                'name': employee.name,
                'job_title ': employee.job_title,
                'work_email': employee.work_email,
                'employee_photo':str(employee.image_1920),
            })
            return {'status': 'Successfully logged in', 'employees_list': employees_dict}


    @restapi.method(
        [(["/get_attendance_status", "/"], "GET")],
        
        auth="user",
    )
    def get_attendance(self):
        user_id = self.env.user
        emp_id = self.env['hr.employee'].search([('user_id','=',user_id.id)])
        if emp_id:
            attendance = self.env['hr.attendance'].search([('check_out','=',False)])
            if attendance:

                return {"employe_name": emp_id.name,'attendance_status':'Marked'}
            else:
                return {"employe_name": emp_id.name,'attendance_status':'Not Marked'} 
        else:
            return {"error": 'No Employee associate with this user please contact to administrator'} 

    
    @restapi.method(
        [(["/mark_employee_checkout"], "POST")],
        
        auth="user",
    )
    def mark_employee_checkout(self):
        params = request.params
        user_id = self.env.user
        emp_id = self.env['hr.employee'].search([('user_id','=',user_id.id)])
        if emp_id:
            attendance = self.env['hr.attendance'].search([('check_out','=',False),('employee_id','=',emp_id.id)])
            if attendance:
                t_date= datetime.datetime.strptime(params.get('date'), "%Y-%m-%d %H:%M:%S")

                attendance.write({'check_out':t_date,
                                  'latitude_2': params.get('latitude_2'),
                                  'longitude_2': params.get('longitude_2'),
                                  'location_2': params.get('location_2'),
                                  })
                return {"employe_name": emp_id.name,'attendance_status':'Success checkout'}
            else:
                return {"employe_name": emp_id.name,'attendance_status':'First Mark attendance'} 
        else:
            return {"error": 'No Employee associate with this user please contact to administrator'} 

        
    
    
    @restapi.method(
        [(["/mark_employee_checkin"], "POST")],
        
        auth="user",
    )
    def mark_employee_checkin(self):
        params = request.params
        user_id = self.env.user
        emp_id = self.env['hr.employee'].search([('user_id','=',user_id.id)])
        if emp_id:
            attendance = self.env['hr.attendance'].search([('check_out','=',False),('employee_id','=',emp_id.id)])
            if not attendance:
                t_date= datetime.datetime.strptime(params.get('date'), "%Y-%m-%d %H:%M:%S")
                attendance_val={
                    'employee_id':emp_id.id,
                    'check_in':t_date,
                    'latitude_1':params.get('latitude_1'),
                    'longitude_1':params.get('longitude_1'),
                    'location_1':params.get('location_1'),
                }

                attendance=self.env['hr.attendance'].create(attendance_val)
                # attendance.write({'check_out':t_date})
                return {"employe_name": emp_id.name,'attendance_status':'Success Checkin'}
            else:
                return {"employe_name": emp_id.name,'attendance_status':'First Checkout attendance'} 
        else:
            return {"error": 'No Employee associate with this user please contact to administrator'} 

    @restapi.method(
        [(["/get_payslip_id"], "GET")],
        
        auth="user",
    )
    def get_payslip_id(self):
        print('get_payslip_id++++++++')
        params = request.params
        user_id = self.env.user
        emp_id = self.env['hr.employee'].search([('user_id','=',user_id.id)])
        if emp_id:
            payslip_date=params.get('year')+'-'+params.get('month')+"-"+'1'
            t_date= datetime.datetime.strptime(payslip_date, "%Y-%m-%d").date()
            payslip_id = self.env['hr.payslip'].search([('date_from','=',t_date),('employee_id','=',emp_id.id)])
            
            if payslip_id:
                base_url = self.env['ir.config_parameter'].sudo().search([('key','=','web.base.url')])
                print('base_url',base_url)
                url=base_url.value+"/my/payslip/download/"+str(payslip_id.id)
                return_val={
                    'employee_id':emp_id.id,
                    'employee_name':emp_id.name,
                    'payslip_id':payslip_id.id,
                    'status':'success',
                    'url':url
                }

                
                return return_val
            else:
                return_val={
                    'employee_id':emp_id.id,
                    'employee_name':emp_id.name,
                    'reason':'Contact Hr for entered month payslip',
                    
                    'status':'failed'
                }

                
                return return_val
                
        else:
            return {"error": 'No Employee associate with this user please contact to administrator'} 

    
    
    


class SessionAuthenticationService(Component):
    _inherit = "base.rest.service"
    _name = "session.authenticate.service"
    _usage = "auth"
    _collection = "session.rest.services"

    def db_monodb(self):
        pass

    @restapi.method([(["/login"], "POST")], auth="public")
    def authenticate(self):
        params = request.params
        db_name = params.get("db", db_monodb())
        request.session.authenticate(db_name, params["login"], params["password"])
        result = request.env["ir.http"].session_info()
        # avoid to rotate the session outside of the scope of this method
        # to ensure that the session ID does not change after this method
        _rotate_session(request)
        request.session.rotate = False
        expiration = datetime.datetime.utcnow() + datetime.timedelta(days=90)
        result["session"] = {
            "sid": request.session.sid,
            "expires_at": fields.Datetime.to_string(expiration),
        }
        return result

    # def db_monodb(self):
    #     pass

    @restapi.method([(["/logout"], "POST")], auth="user")
    def logout(self):

        request.session.logout(keep_db=True)
        return {"message": "Successful logout"}
