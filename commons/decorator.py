from functools import wraps
from flask import request,jsonify
from commons.utils import HttpCodes
from users.models import Users

def verify_token(token):
    query = Users.select(Users.id).where(Users.token==token)
    return list(query.dicts())

def protected(f):
    @wraps(f)
    def decorator(*args, **kws):
            if request.headers.get('Authorization'):
                verify = verify_token(request.headers.get('Authorization'))
                if verify:
                    kws['id'] = verify
                else:
                    return jsonify({"error": HttpCodes.HTTP_401_UNAUTHORIZED}), HttpCodes.HTTP_401_UNAUTHORIZED
            else:
                return jsonify({"error": HttpCodes.HTTP_401_UNAUTHORIZED}), HttpCodes.HTTP_401_UNAUTHORIZED

            return f(*args, **kws)
    return decorator
