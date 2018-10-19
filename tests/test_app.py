import falcon
from falcon import testing
import json
import pytest

from wid.app import api


@pytest.fixture
def client():
    return testing.TestClient(api)


def test_activity_get(client):
    index = 1
    act = {
        'name': 'Practicing techskill',
        'description': 'Pressing buttons until my hands hurt'
    }

    response = client.simulate_get('/activity/{}'.format(index))
    result_doc = json.loads(response.content)

    assert result_doc == act
    assert response.status == falcon.HTTP_OK


def test_activity_post(client):
    act = {
        'name': 'Grind techskill',
        'description': 'Press buttons until hands hurt'
    }

    response = client.simulate_post(
        '/activity',
        json=act
    )

    assert response.status == falcon.HTTP_CREATED
