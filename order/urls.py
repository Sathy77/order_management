from django.urls import path
from order import views
from order import pdf

urlpatterns = [
    path('get-order-summary/', views.getordersummary, name='get-order-summary'),
    path('get-order-items/', views.getorderitems, name='get-order-items'),
    path('add-order/', views.addorder_noauth, name='add-order'),

    path('update-order-status/<int:ordersummaryid>', views.updateorderstatus, name='update-order-status'),

    path('add-order-auth/', views.addorder_auth, name='add-order-auth'),
    path('update-order-auth/<int:ordersummaryid>', views.updateorder_auth, name='update-order-auth'),
    # path('delete-zone/<int:zoneid>', views.deletezone, name='delete-zone'),

    path('ordersummary/pdf/', pdf.generate_ordersummary_pdf, name='generate_ordersummary_pdf'),
]