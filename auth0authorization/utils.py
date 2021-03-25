import json
import os

import jwt
import requests
from django.contrib.auth import authenticate

from dotenv import load_dotenv
load_dotenv(os.path.join('restaurant_project/', '.env'))


def jwt_get_username_from_payload_handler(payload):
    username = payload.get('sub').replace('|', '.')
    authenticate(remote_user=username)
    return username


def jwt_decode_token(token):
    header = jwt.get_unverified_header(token)
    jwks = requests.get(os.environ.get('AUTH0_DOMAIN') + '.well-known/jwks.json').json()
    public_key = None
    for jwk in jwks['keys']:
        if jwk['kid'] == header['kid']:
            public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))

    if public_key is None:
        raise Exception('Public key not found.')

    issuer = os.environ.get('AUTH0_DOMAIN')
    audience = os.environ.get('AUTH0_DOMAIN') + 'userinfo'
    result = jwt.decode(token, public_key, audience=audience, issuer=issuer, algorithms=['RS256'])
    return result
