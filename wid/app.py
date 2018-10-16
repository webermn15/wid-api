import falcon

from .resources import Activity

api = application = falcon.API()

activity_resource = Activity()
api.add_route('/activity/{act_id}', activity_resource)
api.add_route('/activity', activity_resource)
