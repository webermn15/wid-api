import falcon
from .resources import Activity, CreateUser, AuthenticateUser
from .middleware import CORSComponent

api = application = falcon.API(middleware=[CORSComponent()])

activity_resource = Activity()
create_user = CreateUser()
authenticate_user = AuthenticateUser()

api.add_route('/activity/{act_id:int}', activity_resource)
api.add_route('/activity', activity_resource)
api.add_route('/create', create_user)
api.add_route('/login', authenticate_user)
