from django.contrib import admin
from otp import models

# Register your models here.
admin.site.register([
    models.Otp,
])