from django.urls import path
from order import views

urlpatterns = [
    path('add-order-items/', views.addorderitems, name='add-order-items'),
    # path('add-zone/', views.addzone, name='add-zone'),
    # path('update-zone/<int:zoneid>', views.updatezone, name='update-zone'),
    # path('delete-zone/<int:zoneid>', views.deletezone, name='delete-zone'),
]