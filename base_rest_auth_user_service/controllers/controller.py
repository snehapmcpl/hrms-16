from odoo.addons.base_rest.controllers import main
from odoo.http import content_disposition, request, route, serialize_exception

class MyRestController(main.RestController):
    _root_path = '/my_services_api/'
    _collection_name = 'base_rest_auth_user_service.services'

    