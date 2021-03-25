from functools import wraps
import jwt

from django.http import JsonResponse

from users.constants import CLAIMS


def get_token_auth_header(request):
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.META.get("HTTP_AUTHORIZATION", None)
    parts = auth.split()
    token = parts[1]

    return token


def requires_scope(required_scope):
    def require_scope(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            for r in required_scope:
                token = get_token_auth_header(args[0])
                decoded = jwt.decode(token, verify=False)
                if decoded.get(CLAIMS['roles']):
                    roles = decoded.get(CLAIMS['roles'])
                    if roles:
                        for token_scope in roles:
                            if token_scope == r:
                                return f(*args, **kwargs)
            response = JsonResponse({'message': 'You don\'t have access to this resource'})
            response.status_code = 403
            return response

        return decorated

    return require_scope
