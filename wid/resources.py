import json
import falcon
from falcon.media.validators import jsonschema
from wid.schemas import load_schema
from wid.db.db import Database
from wid.utils import format_activities, format_activities_j

psql = Database()


class CreateUser(object):

    @jsonschema.validate(load_schema('user_schema'))
    def on_post(self, req, resp):
        username = req.media.get('username')
        password = req.media.get('password')

        created = psql.create_user(username, password)

        if created is not None:
            print('yes.')
            resp.status = falcon.HTTP_201
            resp.body = json.dumps({'you': 'did it'})
        else:
            print('no.')
            resp.status = falcon.HTTP_400


class AuthenticateUser(object):

    @jsonschema.validate(load_schema('user_schema'))
    def on_post(self, req, resp):
        username = req.media.get('username')
        password = req.media.get('password')

        authenticated = psql.authenticate_user(username, password)

        if authenticated:
            user_act = psql.get_all_user_activities(authenticated)
            user_act_json = [format_activities_j(act) for act in user_act]
            user_json = {
                'user_id': authenticated,
                'username': username,
                'activityList': user_act_json
            }
            resp.status = falcon.HTTP_200
            resp.body = json.dumps({'user': user_json})
        else:
            resp.status = falcon.HTTP_400
            resp.body = json.dumps({'error': 'error message'})


class Activity(object):

    def on_get(self, req, resp, act_id):
        act = psql.get_activity(act_id)

        data = {
            'name': act[1],
            'description': act[2]
        }

        resp.body = json.dumps(data)
        resp.status = falcon.HTTP_200

    @jsonschema.validate(load_schema('activity_schema'))
    def on_post(self, req, resp):
        name = req.media.get('name')
        description = req.media.get('description')

        # all_activities = psql.create_activity(name, description)

        data = format_activities(psql.create_activity(name, description))

        if data is not None:
            resp.status = falcon.HTTP_201
            resp.body = json.dumps(data)
        else:
            resp.status = falcon.HTTP_400
