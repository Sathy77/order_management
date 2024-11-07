from django.urls import path
from otp import views

urlpatterns = [
    path('generate-otp/', views.generate_otp, name='generate-otp'),
    # path('verify-otp/', views.verify_otp, name='verify-otp'),
]