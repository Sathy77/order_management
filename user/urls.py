from django.urls import path
from user import views

urlpatterns = [
    path('get-user/', views.getusers, name='get-user'),
    path('add-user/', views.adduser, name='add-user'),
    path('update-user/<int:uuserid>', views.updateuser, name='update-user'),
    path('delete-user/<int:uuserid>', views.deleteuser, name='delete-user'),
]