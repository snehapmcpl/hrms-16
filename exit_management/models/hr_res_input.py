# -*- coding:utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class HrSettlementInput(models.Model):
    _name = 'hr.settlement.input'
    _description = 'Settlement Input'
    _order = 'settlement_id, sequence'

    name = fields.Char(string="Description")
    settlement_id = fields.Many2one('hr.resignation', string='Pay Slip', required=True, ondelete='cascade', index=True)
    sequence = fields.Integer(required=True, index=True, default=10)
    # _allowed_input_type_ids = fields.Many2many('hr.settlement.input.type', related='settlement_id.struct_id.input_line_type_ids')
    input_type_id = fields.Many2one('hr.settlement.input.type', string='Type', required=True, domain="[('struct_ids', '=', False)]") #'|', ('id', 'in', _allowed_input_type_ids),
    code = fields.Char(related='input_type_id.code', required=True, help="The code that can be used in the salary rules")
    amount = fields.Float(
        string="Count",
        help="It is used in computation. E.g. a rule for salesmen having 1%% commission of basic salary per product can defined in expression like: result = inputs.SALEURO.amount * contract.wage * 0.01.")
    contract_id = fields.Many2one(
        related='settlement_id.contract_id', string='Contract', required=True,
        help="The contract this input should be applied to")


class HrSettlementInputType(models.Model):
    _name = 'hr.settlement.input.type'
    _description = 'Payslip Input Type'

    name = fields.Char(string='Description', required=True)
    code = fields.Char(required=True, help="The code that can be used in the salary rules")
    struct_ids = fields.Many2many('hr.payroll.structure', string='Availability in Structure', help='This input will be only available in those structure. If empty, it will be available in all payslip.')
    country_id = fields.Many2one('res.country', string='Country', default=lambda self: self.env.company.country_id)
