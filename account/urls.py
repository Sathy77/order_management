from django.urls import path
from account import views

urlpatterns = [
    path('get-income/', views.getincomes, name='get-income'),
    path('add-income/', views.addincome, name='add-income'),
    path('update-income/<int:incomeid>', views.updateincome, name='update-income'),
    path('delete-income/<int:incomeid>', views.deleteincome, name='delete-income'),

    path('get-expense/', views.getexpenses, name='get-expense'),
    path('add-expense/', views.addexpense, name='add-expense'),
    path('update-expense/<int:expenseid>', views.updateexpense, name='update-expense'),
    path('delete-expense/<int:expenseid>', views.deleteexpense, name='delete-expense'),

    path('get-transection/', views.gettransections, name='get-transection'),
    path('add-transection/', views.addtransection, name='add-transection'),
    path('update-transection/<int:transectionid>', views.updatetransection, name='update-transection'),

    # path('add-transection-expense/', views.addtransectionexpense, name='add-transection-expense'),
    
]