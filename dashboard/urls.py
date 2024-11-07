from django.urls import path
from dashboard import views

urlpatterns = [
    path('get-monthly-sales-amount/', views.getmonthlysalesamount, name='get-monthly-sales-amount'),
    path('get-monthly-profit/', views.getmonthlyprofit, name='get-monthly-profit'),
    path('get-monthly-location-wise-sale/', views.getmonthlylocationwisesale, name='aget-monthly-location-wise-sale'),
    path('get-monthly-item-wise-sales/', views.getmonthlyitemwisesales, name='get-monthly-item-wise-sales'),
]