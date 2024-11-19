from django.urls import path
from pdf import views

urlpatterns = [
    path('get-orders-pdf/', views.get_orders_pdf, name='get-orders-pdf'),
    path('get-customers-pdf/', views.get_customers_pdf, name='get-customers-pdf'),
    path('get-transections-pdf/', views.get_transections_pdf, name='get-transections-pdf'),
    path('get-products-pdf/', views.get_products_pdf, name='get-products-pdf'),
]