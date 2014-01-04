from flask import abort, request, jsonify, make_response, session
from datetime import datetime, timedelta
from backend.api import app
from backend.api.functions import *

@app.route('/api/signup/', methods = ['POST'])
@require_csrf_token
def api_user_signup(csrf):
    status = {}
    httpcode = 200

    if 'email' in request.json and 'password' in request.json:
        if register_user(request.json['email'], request.json['password']):
            status['code'] = 0
            status['message'] = 'Success'
        else:
            status['code'] = 5 
            status['message'] = 'Could not register user, maybe user already exists?'

    else:
        status['code'] = 3
        status['message'] = 'Missing paramter(s)'
        httpcode = 400

    return make_response(jsonify({ 'csrf_token': csrf, 'status': status }), httpcode)

@app.route('/api/login/', methods = ['POST'])
@require_csrf_token
def api_user_login(csrf):
    status = {}
    httpcode = 200

    if 'email' in request.json and 'password' in request.json:
        id = check_user_credentials(request.json['email'], request.json['password'])
        if id is not None:
            session['id'] = id
            session['loggedin'] = True
            status['code'] = 0
            status['message'] = 'Success'
        else:
            status['code'] = 4
            status['message'] = 'Email and password combination did not match'
    else:
        status['code'] = 3
        status['message'] = 'Missing paramter(s)'
        httpcode = 400

    return make_response(jsonify({ 'csrf_token': csrf, 'status': status }), httpcode)

@app.route('/api/logout/', methods = ['POST'])
@require_authentication
@require_csrf_token
def api_user_logout(csrf):
    session['loggedin'] = False
    response = make_response(jsonify({ 'status': {'code': 0, 'message': 'Sucess'}}), 200)
    return response

@app.route('/api/')
def api_root():
    generate_csrf_token(session)
    
    status = {'code': 0, 'message': 'Sucess'}
    response = make_response(jsonify({'csrf_token': session['csrf'], 'status': status}), 200)
    return response

@app.route('/api/subscribe/', methods = ['POST'])
@require_authentication
@require_csrf_token
def api_subscribe(csrf):
    status = {}
    httpcode = 200
    feed = None

    if 'url' in request.json and 'name' in request.json:
        feed = add_feed(request.json['url'])
        subscribe_user(session['id'], feed, request.json['name'])
        status['code'] = 0
        status['message'] = 'Success'
    else:
        status['code'] = 3
        status['message'] = 'Missing paramter(s)'
        httpcode = 400

    return make_response(jsonify({ 'csrf_token': csrf, 'feed_id': feed, 'status': status }), httpcode)

