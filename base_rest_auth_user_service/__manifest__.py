# Copyright 2021 Wakari SRL (http://www.wakari.be)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    "name": "REST Authentication Service",
    "summary": "Login/logout from session using a REST call",
    "version": "15.0.1.0.2",
    "development_status": "Alpha",
    "license": "LGPL-3",
    "website": "https://github.com/OCA/rest-framework",
    "author": "Wakari, Odoo Community Association (OCA)",
    "depends": ["base_rest","portal","om_hr_payroll"],
    "data": ["views/hr_attendance.xml"],
    "installable": True,
}
