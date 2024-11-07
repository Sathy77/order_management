from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
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
