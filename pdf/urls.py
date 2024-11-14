from django.urls import path
from pdf import views

urlpatterns = [
    path('get-orders-pdf/', views.get_orders_pdf, name='get-orders-pdf'),
    path('get-customers-pdf/', views.get_customers_pdf, name='get-customers-pdf'),
    path('get-transections-pdf/', views.get_transections_pdf, name='get-transections-pdf'),
    path('get-products-pdf/', views.get_products_pdf, name='get-products-pdf'),
    # path('add-user/', views.adduser, name='add-user'),
    # path('update-user/<int:uuserid>', views.updateuser, name='update-user'),
    # path('delete-user/<int:uuserid>', views.deleteuser, name='delete-user'),

    # path('add-customer/', views.addcustomer, name='add-customer'),
    # path('get-customer/', views.getcustomers, name='get-customer'),
    # path('update-customer/<int:customerid>', views.updatecustomer, name='update-customer'),
    # path('delete-customer/<int:customerid>', views.deletecustomer, name='delete-customer'),

    # path('get-permission/', views.getpermissions, name='get-permission'),
    # path('add-permission/', views.addpermission, name='add-permission'),
    # path('update-permission/<int:permissionid>', views.updatepermission, name='update-permission'),
    # path('delete-permission/<int:permissionid>', views.deletepermission, name='delete-permission'),

    # path('get-role/', views.getroles, name='get-role'),
    # path('add-role/', views.addrole, name='add-role'),
    # path('update-role/<int:roleid>', views.updaterole, name='update-role'),
    # path('delete-role/<int:roleid>', views.deleterole, name='delete-role'),

    # path('get-permission-category/', views.getpermissioncategory, name='get-permission-category'),
]