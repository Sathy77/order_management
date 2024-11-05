from django.urls import path
from dashboard import views

urlpatterns = [
    path('get-monthly-sales-amount/', views.getmonthlysalesamount, name='aget-monthly-sales-amount'),
    path('get-monthly-profit/', views.getmonthlyprofit, name='aget-monthly-profit'),
    path('get-monthly-location-wise-sale/', views.getmonthlylocationwisesale, name='aget-monthly-location-wise-sale'),
]