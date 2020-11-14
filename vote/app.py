from flask import Flask, render_template, request, make_response, g
from redis import Redis
import os
import socket
import random
import json

option_a = os.getenv('OPTION_A', "Cats")
option_b = os.getenv('OPTION_B', "Dogs")

REDIS_PASSWORD= os.environ['REDIS_PASS']
REDIS_HOST= os.environ['REDIS_HOST']
REDIS_PORT= os.environ['REDIS_PORT']

PORT = int(os.environ.get("PORT", 5050))

hostname = socket.gethostname()

#redis://default:password@host:port

app = Flask(__name__)

def get_redis(REDIS_HOST, REDIS_PASSWORD, REDIS_PORT):
    if not hasattr(g, 'redis'):
        g.redis = Redis(
            host= REDIS_HOST, 
            port= REDIS_PORT, 
            password= REDIS_PASSWORD,
            socket_timeout=5)
    return g.redis


@app.route("/", methods=['POST', 'GET'])
def hello():
    voter_id = get_voter()

    vote = countvote(None, voter_id)

    resp = make_response(render_template(
        'index.html',
        option_a=option_a,
        option_b=option_b,
        hostname=hostname,
        vote=vote,
    ))
    resp.set_cookie('voter_id', voter_id)
    return resp


@app.route("/", methods=['POST', 'GET'])
def countvote(vote, voter_id):

    if request.method == 'POST':
        redis = get_redis()
        vote = request.form['vote']
        data = json.dumps({'voter_id': voter_id, 'vote': vote})
        redis.rpush('votes', data)
    return vote


@app.route("/", methods=['POST', 'GET'])
def get_voter():
    voter_id = request.cookies.get('voter_id')
    if not voter_id:
        print('Usuario nuevo')
        voter_id = hex(random.getrandbits(64))[2:-1]
    return voter_id


if name == "main":
    app.run(host='0.0.0.0', threaded=True, port=PORT)