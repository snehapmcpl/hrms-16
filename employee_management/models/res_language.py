from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError


class Language(models.Model):
    _name = 'res.language'

    speak_lang = fields.Boolean(string="Speak")
    langauge_name = fields.Char(string="Language Name")
    write_lang = fields.Boolean(string="Write")
    employee_language = fields.Many2one('hr.employee')
    read_lang = fields.Boolean(string="Read")