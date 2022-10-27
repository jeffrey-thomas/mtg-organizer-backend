from functools import wraps
from flask import request, jsonify, json
import decimal
from firebase_admin import auth

def token_required(flask_function):
    @wraps(flask_function)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(' ')[1]

        if not token:
            return jsonify({'message':'Token is missing.'}), 401

        #try:
        user_token = auth.verify_id_token(token)
        uid = user_token['uid']
        #except:
        #    return jsonify({'message':'Token is invalid.'})

        return flask_function(uid, *args, **kwargs)
    return decorated

class JSONEncoder(json.JSONEncoder):
    def default(self,obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return super(JSONEncoder,self).default(obj)