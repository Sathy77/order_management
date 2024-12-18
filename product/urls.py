from django.urls import path
from product import views

urlpatterns = [
    path('get-product/', views.getproducts_noauth, name='get-product'),
    path('add-product/', views.addproduct, name='add-product'),
    path('update-product/<int:productid>', views.updateproduct, name='update-product'),
    path('delete-product/<int:productid>', views.deleteproduct, name='delete-product'),
    
    path('get-product-auth/', views.getproducts_auth, name='get-product-auth'),
]