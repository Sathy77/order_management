from django.urls import path
from zone import views

urlpatterns = [
    path('get-delivery-zone/', views.getdeliveryzones, name='get-delivery-zone'),
    path('add-delivery-zone/', views.adddeliveryzone, name='add-delivery-zone'),
    path('update-delivery-zone/<int:deliveryzoneid>', views.updatedeliveryzone, name='update-delivery-zone'),
    path('delete-delivery-zone/<int:deliveryzoneid>', views.deletedeliveryzone, name='delete-delivery-zone'),
]