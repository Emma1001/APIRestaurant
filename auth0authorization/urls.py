from django.urls import path

from . import views

urlpatterns = [
    path('api/public', views.public),
    path('api/private', views.private),
    path('api/create-order', views.create_order),
    path('api/edit-order', views.edit_order),
    path('api/serve-table', views.serve_table),
    path('api/add-items', views.add_items),
    path('api/see-order', views.see_order),
    path('api/delete-order', views.delete_order),
    path('api/add-menu-items', views.add_menu_items),
    path('api/create-order-roles', views.create_order_roles),
]