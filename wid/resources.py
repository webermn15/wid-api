import json
import falcon
from falcon.media.validators import jsonschema
from wid.schemas import load_schema
from wid.db import Database

psql = Database()


class Activities(object):

    def on_get(self, req, resp):
        act = {
            'name': 'Grind techskill',
            'description': 'Press buttons until hands hurt'
        }

        resp.body = json.dumps(act)

        resp.status = falcon.HTTP_200

    @jsonschema.validate(load_schema('activity_creation'))
    def on_post(self, req, resp):
        name = req.media.get('name')
        description = req.media.get('description')

        resp.status = falcon.HTTP_201
