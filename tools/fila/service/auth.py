from flask import g, request, abort, make_response, jsonify
import config
import jwt
from functools import wraps

def jwt_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_claims = get_user_claims()
        if not user_claims:
            abort(make_response(jsonify(message="Unauthorized"), 401))
        return f(*args, **kwargs)
    return decorated_function


def get_user_claims():
    try:
        if g.user_claims == None:
            raise AttributeError()
    except AttributeError:
        try:
            parts = request.headers.get('Authorization').split()
            if parts[0] != "Bearer":
                raise jwt.exceptions.DecodeError()
            g.user_claims = jwt.decode(parts[1], config.SECRET_KEY, algorithms=['HS256'])
        except (jwt.exceptions.DecodeError, IndexError, AttributeError, jwt.exceptions.ExpiredSignatureError): 
            g.user_claims = None
    return g.user_claims