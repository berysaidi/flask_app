'''
These are the endpoints which Flask takes care of to route the request to their handlers.
'''
from re import search
from csv import reader
from json import loads, decoder
from flask import request, jsonify, make_response
from jsonschema import validate, ValidationError
from werkzeug.exceptions import HTTPException
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

from app import app, cache
from app.schema import SCHEMA


@cache.cached()
def read_macs():
    ''' Caching Mac addresses to speedup retrieval '''
    with open("mac.csv", newline='', encoding='utf-8') as file:
        data = reader(file, delimiter=',')
        macs = []
        for row in data:
            macs.append(row[0])
        # get rid of title
        macs.pop(0)
        return macs

@app.route("/login", methods=["POST"])
def login():
    ''' Create a route to authenticate your users and return JWTs. The
        create_access_token() function is used to actually generate the JWT.
        the user trying to post its profile must use
    '''
    try:
        client = request.headers['x-client-id']
    except KeyError:
        return make_response({'statusCode': 401, 'error': 'Conflict',
                             'message': 'invalid clientId or token supplied'}), 401

    # TODO : check clientID in db
    if client != "client":
        return make_response({'statusCode': 401, 'error': 'Conflict',
                             'message': 'invalid clientId or token supplied'}), 401

    access_token = create_access_token(identity=client)
    return jsonify(access_token=access_token)


@app.route('/profiles/clientId:<mac>', methods=['POST'])
@jwt_required()
def post_profile(mac):
    ''' Protect a route with jwt_required, which will kick out requests
    without a valid JWT present. '''
    # Check the header information
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    # TODO: check clientID in db
    if current_user != 'client':
        return make_response({'statusCode': 401, 'error': 'Conflict',
                             'message': 'invalid clientId or token supplied'}), 401

    # check mac address format and availability
    match = search(r"([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}", mac)
    macs = read_macs()
    if (not match) or (mac not in macs):
        return make_response({'statusCode': 404, 'error': 'Not Found',
                             'message': 'profile of client %s does not exist' % mac}), 404

    # Check the body information
    try:
        data = loads(request.data)
        validate(instance=data, schema=SCHEMA)
    except ValidationError:
        return make_response(
            {'statusCode': 409, 'error': 'Conflict', 'message': 'data error'}), 409
    except decoder.JSONDecodeError:
        return make_response(
            {'statusCode': 409, 'error': 'Conflict', 'message': 'error unmarshalling json'}), 409

    # After all Validation is done, we can safely return a proper OK 200
    return make_response(jsonify(data)), 200


@app.errorhandler(Exception)
def handle_exception(err):
    ''' Exception Handler for uncaught errors to avoid embarassing ourselves ! '''

    # pass through HTTP errors
    if isinstance(err, HTTPException):
        return err

    # now handling non-HTTP exceptions only
    return make_response({'statusCode': 500, 'error': 'Internal Server Error',
                         'message': 'An internal server error occured'}), 500
