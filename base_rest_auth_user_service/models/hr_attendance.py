from odoo import api, Command, fields, models, _

class HrAttendance(models.Model):
    _inherit = 'hr.attendance'


    latitude_1 = fields.Char(string="Latitude 1")
    longitude_1 = fields.Char(string="Longitude 1")
    location_1 = fields.Char(string="Location 1")
    latitude_2 = fields.Char(string="Latitude 2")
    longitude_2 = fields.Char(string="Longitude 2")
    location_2 = fields.Char(string="Location 2")