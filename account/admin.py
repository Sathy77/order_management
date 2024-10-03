from django.contrib import admin
from account import models

# Register your models here.
admin.site.register([
    models.Income,
    models.Expense,
    models.Transectionincome,
    models.Transectionexpense,
])