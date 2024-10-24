from django.urls import path
from om_settings import views

urlpatterns = [
    path('get-setting/', views.getsettings, name='get-setting'),
    # path('add-setting/', views.addsetting, name='add-setting'),
    path('update-setting/<int:settingid>', views.updatesetting, name='update-setting'),
    # path('delete-zone/<int:zoneid>', views.deletezone, name='delete-zone'),
]