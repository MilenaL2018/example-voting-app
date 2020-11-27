from flask import Flask, render_template, request, make_response, g
from redis import Redis
import os
import socket
import random
import json

option_a = os.getenv('OPTION_A', "Cats")
option_b = os.getenv('OPTION_B', "Owls")

REDIS_PASSWORD= os.environ.get('REDIS_PASSWORD', '123')
REDIS_HOST= os.environ.get('REDIS_HOST', 'host')
REDIS_PORT= os.environ.get('REDIS_PORT', '5000')


PORT = int(os.environ.get("PORT", 5000))

hostname = socket.gethostname()

app = Flask(__name__)

def get_redis(REDIS_HOST, REDIS_PASSWORD, REDIS_PORT):
    if not hasattr(g, 'redis'):
        try:
            g.redis = Redis(
                host=REDIS_HOST, 
                port=REDIS_PORT,
                password=REDIS_PASSWORD,
                socket_timeout=5)
        except Exception as ex:
            print('Error:', ex)
            g.redis = None
    return g.redis

@app.route("/", methods=['POST', 'GET'])
def hello():
    voter_id = get_voter(request.cookies.get('voter_id'))

    vote = count_vote(None, voter_id)

    resp = make_response(render_template(
        'index.html',
        option_a=option_a,
        option_b=option_b,
        hostname=hostname,
        vote=vote,
    ))
    resp.set_cookie('voter_id', voter_id)
    return resp

def count_vote(vote, voter_id):
    if request.method == 'POST':
        redis = get_redis(REDIS_HOST=REDIS_HOST, REDIS_PASSWORD=REDIS_PASSWORD, REDIS_PORT=REDIS_PORT)
        vote = request.form['vote']
        data = json.dumps({'voter_id': voter_id, 'vote': vote})
        redis.rpush('votes', data)
    return vote

def get_voter(voter_id):
    voter_id = voter_id
    if not voter_id:
        print('Usuario nuevo')
        voter_id = hex(random.getrandbits(64))[2:-1]
    return voter_id

if __name__ == "__main__":
    app.run(host='0.0.0.0', threaded=True, port=PORT)