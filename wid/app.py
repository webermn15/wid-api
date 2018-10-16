import falcon

from .resources import Activities

api = application = falcon.API()

activitylist = Activities()
api.add_route('/', activitylist)
