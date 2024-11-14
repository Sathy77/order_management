from django.contrib import admin
from om_settings import models

# Register your models here.
admin.site.register([
    models.Settings,
    
])