import os
import tempfile

import pytest

from flaskr import flaskr
from flask import request, jsonify

@app.route('/api/auth')
def auth():
    json_data = request.get_json()
    voter_id = json_data['voter_id']
    vote = json_data['vote']
    return jsonify(voter_id, vote)

    with app.test_client() as c:
        rv = c.post('/api/auth', json={
            'voter_id': 'mock voter', 'vote': 'option_a'
        })
        json_data = rv.get_json()
        assert verify_token(data, json_data['token'])


@pytest.fixture
def client():
    db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
    flaskr.app.config['TESTING'] = True

    with flaskr.app.test_client() as client:
        with flaskr.app.app_context():
            flaskr.init_db()
        yield client

    os.close(db_fd)
    os.unlink(flaskr.app.config['DATABASE'])

def test_empty_db(client):
    """Start with a blank database."""

    rv = client.get('/')
    assert b'No entries here so far' in rv.data