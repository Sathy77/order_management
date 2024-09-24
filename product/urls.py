from django.urls import path
from product import views

urlpatterns = [
    path('get-product/', views.getproducts, name='get-product'),
    path('add-product/', views.addproduct, name='add-product'),
    # path('update-user/<int:uuserid>', views.updateuser, name='update-user'),
    # path('delete-user/<int:uuserid>', views.deleteuser, name='delete-user'),
]