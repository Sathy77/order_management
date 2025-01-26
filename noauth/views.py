from django.shortcuts import render
from rest_framework.decorators import api_view
from user import models as MODELS_USER
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET'])
def createUser(request, username=None, password=None):
    try:
        if username and password:
            user = MODELS_USER.User.objects.create_superuser(username=username, password=password)
            user.user_type='Admin'
            user.save()
            return Response({'message': 'User created!', 'username': username, 'password': password}, status=status.HTTP_201_CREATED)
        else:
            user = MODELS_USER.User.objects.create_superuser(username='admin', password='admin')
            user.user_type='Admin'
            user.save()
            return Response({'message': 'User created!', 'username': 'admin', 'password': 'admin'}, status=status.HTTP_201_CREATED)
    except: return Response({'message': 'Couldn\'t create user!', 'username': '', 'password': ''}, status=status.HTTP_400_BAD_REQUEST)