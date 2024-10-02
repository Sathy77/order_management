from django.urls import path
from user import views

urlpatterns = [
    path('get-user/', views.getusers, name='get-user'),
    path('add-user/', views.adduser, name='add-user'),
    path('update-user/<int:uuserid>', views.updateuser, name='update-user'),
    path('delete-user/<int:uuserid>', views.deleteuser, name='delete-user'),

    path('add-customer/', views.addcustomer, name='add-customer'),
    path('get-customer/', views.getcustomers, name='get-customer'),
    path('update-customer/<int:customerid>', views.updatecustomer, name='update-customer'),
    path('delete-customer/<int:customerid>', views.deletecustomer, name='delete-customer'),
]