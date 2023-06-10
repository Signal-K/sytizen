import os
import tempfile

import pytest
from app import app

@pytest.fixture
def client():
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])


def test_authenticate(client):
    response = client.post('/authenticate')
    assert response.status_code == 200
    assert b'Token' in response.data


def test_get_data(client):
    response = client.get('/get_data')
    assert response.status_code == 200
    assert b'data' in response.data


def test_post_data(client):
    response = client.post('/post_data', json={'planetId': '52', 'image': 'link_to_image', 'name': 'KOI-7923', 'radius': 1.0, 'orbital_period': 365.25})
    assert response.status_code == 200
    assert b'success' in response.data


def test_generate_lightcurve(client):
    response = client.post('/generate_lightcurve', json={'tic_id': 'KOI-7923'})
    assert response.status_code == 200
    assert b'success' in response.data