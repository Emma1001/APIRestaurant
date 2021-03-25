import jwt
from rest_framework.permissions import BasePermission

from auth0authorization.decorators import get_token_auth_header
from users.constants import CLAIMS, ADMIN_ROLE, BARTENDER_ROLE, WAITER_ROLE


class CreateOrder(BasePermission):
    def has_permission(self, request, view):
        token = get_token_auth_header(request)
        decoded = jwt.decode(token, verify=False)
        roles = decoded.get(CLAIMS['roles'])
        if roles:
            role = roles[0]
            if role == ADMIN_ROLE or role == BARTENDER_ROLE or role == WAITER_ROLE:
                return True


class EditOrder(BasePermission):
    def has_permission(self, request, view):
        token = get_token_auth_header(request)
        decoded = jwt.decode(token, verify=False)
        roles = decoded.get(CLAIMS['roles'])
        if roles:
            role = roles[0]
            if role == ADMIN_ROLE or role == BARTENDER_ROLE or role == WAITER_ROLE:
                return True

class ServeTable(BasePermission):
    def has_permission(self, request, view):
        token = get_token_auth_header(request)
        decoded = jwt.decode(token, verify=False)
        roles = decoded.get(CLAIMS['roles'])
        if roles:
            role = roles[0]
            if role == ADMIN_ROLE or role == WAITER_ROLE:
                return True

class AddItemToOrder(BasePermission):
    def has_permission(self, request, view):
        token = get_token_auth_header(request)
        decoded = jwt.decode(token, verify=False)
        roles = decoded.get(CLAIMS['roles'])
        if roles:
            role = roles[0]
            if role == WAITER_ROLE:
                return True


class SeeWaitersOrder(BasePermission):
    def has_permission(self, request, view):
        token = get_token_auth_header(request)
        decoded = jwt.decode(token, verify=False)
        roles = decoded.get(CLAIMS['roles'])
        if roles:
            role = roles[0]
            if role == ADMIN_ROLE or role == BARTENDER_ROLE or role == WAITER_ROLE:
                return True

class DeleteOrder(BasePermission):
    def has_permission(self, request, view):
        token = get_token_auth_header(request)
        decoded = jwt.decode(token, verify=False)
        roles = decoded.get(CLAIMS['roles'])
        if roles:
            role = roles[0]
            if role == ADMIN_ROLE or role == BARTENDER_ROLE:
                return True

class AddMenuItems(BasePermission):
    def has_permission(self, request, view):
        token = get_token_auth_header(request)
        decoded = jwt.decode(token, verify=False)
        roles = decoded.get(CLAIMS['roles'])
        if roles:
            role = roles[0]
            if role == ADMIN_ROLE:
                return True

class CreateOrderRoles(BasePermission):
    def has_permission(self, request, view):
        token = get_token_auth_header(request)
        decoded = jwt.decode(token, verify=False)
        roles = decoded.get(CLAIMS['roles'])
        if roles:
            role = roles[0]
            if role == ADMIN_ROLE:
                return True
