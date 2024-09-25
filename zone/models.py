from django.db import models
from helps.abstract.abstractclass import Basic
from django.core.validators import MinValueValidator, MaxValueValidator
from helps.common.generic import Generichelps as ghelp
from user import models as MODELS_USER

# Create your models here.

class Deliveryzone(Basic):
    name  = models.CharField(max_length=200, blank=True, null=True)
    cost = models.FloatField(validators=[MinValueValidator(0)], blank=True, null=True)

    created_by = models.ForeignKey(MODELS_USER.User, on_delete=models.SET_NULL, null=True, blank=True, related_name='zone_created_by')
    updated_by = models.ForeignKey(MODELS_USER.User, on_delete=models.SET_NULL, null=True, blank=True, related_name='zone_updated_by')

    def __str__(self):
        return f'{self.name} - {self.cost}' 
