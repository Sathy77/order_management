from django.urls import path
from order import views

urlpatterns = [
    path('get-order-summary/', views.getordersummary, name='get-order-summary'),
    path('get-order-items/', views.getorderitems, name='get-order-items'),
    path('add-order-items/', views.addorderitems, name='add-order-items'),

    path('update-order-summary-status/<int:ordersummaryid>', views.updateordersummarystatus, name='update-order-summary-status'),
    # path('delete-zone/<int:zoneid>', views.deletezone, name='delete-zone'),
]