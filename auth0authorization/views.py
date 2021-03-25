from django.shortcuts import render

from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from auth0authorization.decorators import requires_scope


@api_view(['GET'])
@permission_classes([AllowAny])
def public(request):
    return JsonResponse({'message': 'Hello from a public endpoint! You don\'t need to be authenticated to see this.'})


@api_view(['GET'])
def private(request):
    return JsonResponse({'message': 'Hello from a private endpoint! You need to be authenticated to see this.'})


@api_view(['POST'])
@requires_scope(['Bartender', 'Waiter', 'Admin'])
def create_order(request):
    return JsonResponse({
        'message': 'You can create orders'})


@api_view(['PATCH'])
@requires_scope(['Bartender', 'Waiter', 'Admin'])
def edit_order(request):
    return JsonResponse({
        'message': 'You can edit orders'})


@api_view(['POST'])
@requires_scope(['Waiter', 'Admin'])
def serve_table(request):
    return JsonResponse({
        'message': 'You can serve each table'})


@api_view(['POST'])
@requires_scope(['Waiter'])
def add_items(request):
    return JsonResponse({
        'message': 'You can add items to order but not to remove items/orders'})


@api_view(['GET'])
@requires_scope(['Waiter', 'Bartender', 'Admin'])
def see_order(request):
    return JsonResponse({
        'message': 'You can see waiter\'s orders'})


@api_view(['DELETE'])
@requires_scope(['Bartender', 'Admin'])
def delete_order(request):
    return JsonResponse({
        'message': 'You can soft delete orders'})


@api_view(['POST'])
@requires_scope(['Admin'])
def add_menu_items(request):
    return JsonResponse({
        'message': 'You can add menu items'})


@api_view(['POST'])
@requires_scope(['Admin'])
def create_order_roles(request):
    return JsonResponse({
        'message': 'You can create order roles'})
