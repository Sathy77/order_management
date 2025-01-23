from django.urls import path
from noauth import views

urlpatterns = [
    path('__create-super-user__/<str:username>/<str:password>', views.createUser, name='__create-super-user__')
]