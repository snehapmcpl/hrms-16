from odoo import models, fields, _, api
from odoo.exceptions import UserError


class HrEmployeeTax(models.Model):
    _name = "hr.employee.tax"

    name = fields.Char("Name", default=lambda self: self.env['ir.sequence'].next_by_code('hr.employee.tax'), readonly=True)
    employee_id = fields.Many2one("hr.employee", string="Employee")
    section_24 = fields.One2many('section24.lines', 'self_service_section24', string="Section 24")
    section_80c = fields.One2many('section80c.lines', 'self_service_section80c', string="Section 80C")
    chapter_VI_A = fields.One2many('chapter6.lines', 'self_service_chapter6', string="Chapter VI A")
    section_10 = fields.One2many('section10.lines', 'self_service_section10', string="Section 10")
    other_income = fields.One2many('other.income.sources.line', 'self_service_other_income', string="Other Income Sources")


class Section24Lines(models.Model):
    _name = "section24.lines"

    self_service_section24 = fields.Many2one('hr.employee.tax', string="Employee")
    section_24 = fields.Many2one('tax.section24', string="Section 24")
    amount = fields.Float("Amount")
    document = fields.Binary('Document (*)')
    file_name = fields.Char("File Name")

    @api.onchange('document')
    def check_file_type(self):
        if self.document:
            data = self.file_name.split('.')
            if data[-1] != 'pdf':
                raise UserError('Invalid File type... Only PDF is allowed')


class Section80cLines(models.Model):
    _name = 'section80c.lines'

    self_service_section80c = fields.Many2one('hr.employee.tax', string="Employee")
    section_80c = fields.Many2one('tax.section80c', string="Section 80 C")
    amount = fields.Float("Deductible Amount")
    document = fields.Binary('Document (*)')
    file_name = fields.Char("File Name")

    @api.onchange('document')
    def check_file_type(self):
        if self.document:
            data = self.file_name.split('.')
            if data[-1] != 'pdf':
                raise UserError('Invalid File type... Only PDF is allowed')


class Chapter6Lines(models.Model):
    _name = 'chapter6.lines'

    self_service_chapter6 = fields.Many2one('hr.employee.tax', string="Employee")
    chapter6 = fields.Many2one('tax.chapter6', string="Chapter VI A")
    amount = fields.Float("Amount")
    document = fields.Binary('Document (*)')
    file_name = fields.Char("File Name")

    @api.onchange('document')
    def check_file_type(self):
        if self.document:
            data = self.file_name.split('.')
            if data[-1] != 'pdf':
                raise UserError('Invalid File type... Only PDF is allowed')


class Section10Lines(models.Model):
    _name = 'section10.lines'

    self_service_section10 = fields.Many2one('hr.employee.tax', string="Employee")
    section_10 = fields.Many2one('tax.section10', string="Section 10")
    amount = fields.Float("Amount")
    document = fields.Binary('Document (*)')
    file_name = fields.Char("File Name")

    @api.onchange('document')
    def check_file_type(self):
        if self.document:
            data = self.file_name.split('.')
            if data[-1] != 'pdf':
                raise UserError('Invalid File type... Only PDF is allowed')


class OtherIncomeSourcesLines(models.Model):
    _name = 'other.income.sources.line'

    self_service_other_income = fields.Many2one('hr.employee.tax', string="Employee")
    other_incomes = fields.Many2one('other.income.sources', string="Other Income Sources")
    amount = fields.Float("Amount")
