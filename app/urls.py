from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path("" , views.index , name = "index" ),
    path('add-product/', views.add_product, name='add_product'),
    path('product-success/', views.product_success, name='product_sucess'),
    path("tag-dead-stock/", views.tag_dead_stock, name="tag_dead_stock"),
    path("inventory/", views.inventory_view, name="inventory"),
    path("alerts/", views.alerts_view, name="alerts"),
    path("transfer_request/",views.request_transfer_view, name="request_transfer"),
    path('transport-costs/', views.transport_calculator_view, name='transport_costs'),
]
