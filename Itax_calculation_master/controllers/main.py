from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import content_disposition
import base64

class server_connection_controller(http.Controller):
    @http.route('/YTOD_report', type="http", auth="user")
    def YTOD_report_xls(self, **kw):
        id = kw.get('id')
        model = request.env['ytod.wizard']
        obj = model.browse(int(id))
        if obj:
            filecontent = base64.b64decode(obj.data)
            filename = obj.name
            if filecontent and filename:
                return request.make_response(filecontent, headers=[('Content-Type', 'application/octet-stream'),
                                                                   ('Content-Disposition',
                                                                    content_disposition(filename))])
        return request.not_found()
