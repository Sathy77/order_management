from django.urls import path
from zone import views

urlpatterns = [
    path('get-delivery-zone/', views.getdeliveryzones_noauth, name='get-delivery-zone'),
    path('add-delivery-zone/', views.adddeliveryzone, name='add-delivery-zone'),
    path('update-delivery-zone/<int:deliveryzoneid>', views.updatedeliveryzone, name='update-delivery-zone'),
    path('delete-delivery-zone/<int:deliveryzoneid>', views.deletedeliveryzone, name='delete-delivery-zone'),
    
    path('get-delivery-zone-auth/', views.getdeliveryzones_auth, name='get-delivery-zone-auth'),
]