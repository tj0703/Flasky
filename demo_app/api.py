import functools

import base64
import random

from flask import (
    Blueprint, request, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash
from demo_app.db import get_db

bp = Blueprint('api', __name__, url_prefix='/api')

def login_required(call):
    @functools.wraps(call)
    def wrapped_call(*args, **kwargs):
        error = None
        user = None
        auth = request.authorization
        print('auth request: {}'.format(auth))
        if auth:
            user = get_db().execute(
                'SELECT * FROM user WHERE username = ?', (auth.username,)).fetchone()
        if user is None:
            error = 'Invalid User'
        elif not check_password_hash(user['password'], auth.password):
            error = 'Invalid Authentication'

        if error:
            return jsonify({'status': 'FAILURE',
                            'message': error}), 401
        return call(*args, **kwargs)

    return wrapped_call

def token_required(call):
    @functools.wraps(call)
    def wrapped_call(*args, **kwargs):
        headers = request.headers
        if not headers.get('token'):
            return jsonify({'status': 'FAILURE',
                            'message': 'Token authentication required'}), 401

        tokens = [x[0] for x in get_db().execute("SELECT token FROM user").fetchall()]
        if headers.get('token') in tokens:
            return call(*args, **kwargs)
        else:
            return jsonify({'status': 'FAILURE',
                            'message': 'Invalid Token'}), 401

    return wrapped_call

@bp.route('/auth/token', methods=(['GET']))
@login_required
def create_token():
    username = request.authorization.username
    token = str(base64.b64encode(str(random.getrandbits(128)).encode()), "utf-8")
    get_db().execute("UPDATE user SET token = '{}' WHERE username = '{}'".format(token, username))
    get_db().commit()
    return jsonify({'status': 'SUCCESS',
                    'token': token}), 200

@bp.route('/users', methods=(['GET']))
def users():
    """Register a new user.

    Validates that the username is not already taken. Hashes the
    password for security.
    """
    if request.method == 'GET':
        return get_all_users()

@bp.route('/users/<username>', methods=(['GET', 'PUT']))
@token_required
def username(username):
    if request.method == 'GET':
        return get_specific_user(username)
    if request.method == 'PUT':
        return put_specific_user(username, request)

def put_specific_user(username, request):
    allowed_fields = ('firstname', 'lastname', 'phone')
    if not request.is_json:
        return jsonify({'status': 'FAILURE',
                        'message': 'Bad Request'}), 400

    data = request.get_json()
    print(data)
    db = get_db()
    for key, value in data.items():
        if key not in allowed_fields:
            return jsonify({'status': 'FAILURE',
                            'message': 'Field update not allowed'}), 403
        db.execute("UPDATE user SET '{}' = '{}' WHERE username = '{}'".format(key, value, username))
    db.commit()
    return jsonify({'status': 'SUCCESS',
                    'message': 'Updated'}), 201

def get_specific_user(username):
    try:
        query = get_db().execute("""SELECT firstname, lastname, phone
                                    FROM user
                                    WHERE username = '{}'""".format(
                                        username)).fetchall()
    except:
        return jsonify({'status': 'FAILURE',
                        'message': 'user not found'}), 404

    payload = {'firstname': query[0][0],
               'lastname': query[0][1],
               'phone': query[0][2]}
    return jsonify({'status': 'SUCCESS',
                    'message': 'retrieval succesful',
                    'payload': payload}), 200

def get_all_users():

    query = get_db().execute("""SELECT username
                                FROM user""").fetchall()
    users = []
    for item in query:
        users.append(item['username'])
    return jsonify({'status': 'SUCCESS',
                    'payload': users}), 200
