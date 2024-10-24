from django.urls import path
from order import views

urlpatterns = [
    path('get-order-summary/', views.getordersummary, name='get-order-summary'),
    path('get-order-items/', views.getorderitems, name='get-order-items'),
    path('add-order-items/', views.addorderitems_noauth, name='add-order-items'),

    path('update-order-summary-status/<int:ordersummaryid>', views.updateordersummarystatus, name='update-order-summary-status'),

    path('add-order-items-auth/', views.addorderitem_auth, name='add-order-items-auth'),
    path('update-order-item-auth/<int:ordersummaryid>', views.updateorderitem_auth, name='update-order-item-auth'),
    # path('delete-zone/<int:zoneid>', views.deletezone, name='delete-zone'),
]