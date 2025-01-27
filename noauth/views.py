from django.shortcuts import render
from rest_framework.decorators import api_view
from user import models as MODELS_USER
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET'])
def createUser(request, username=None, password=None):
    try:
        # Create the user
        if username and password:
            user = MODELS_USER.User.objects.create_superuser(username=username, password=password)
        else:
            user = MODELS_USER.User.objects.create_superuser(username='admin', password='admin')
        
        # Set user type
        user.user_type = 'Admin'
        user.save()
        
        # Assign all roles to the user
        roles = MODELS_USER.Role.objects.all()
        user.role.set(roles)
        
        return Response({
            'message': 'User created!',
            'username': username or 'admin',
            'password': password or 'admin'
        }, status=status.HTTP_201_CREATED)
    except Exception as e:
        # Return error response with the exception message
        return Response({
            'message': f"Couldn't create user! {str(e)}",
            'username': '',
            'password': ''
        }, status=status.HTTP_400_BAD_REQUEST)
