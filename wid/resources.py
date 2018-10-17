import json
import falcon
from falcon.media.validators import jsonschema
from wid.schemas import load_schema
from wid.db.db import Database
from wid.utils import format_activities

psql = Database()


class Activity(object):

    def on_get(self, req, resp, act_id):
        act = psql.get_activity(act_id)

        data = {
            'name': act[1],
            'description': act[2]
        }

        resp.body = json.dumps(data)
        resp.status = falcon.HTTP_200

    @jsonschema.validate(load_schema('activity_model'))
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
