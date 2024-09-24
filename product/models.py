from django.db import models
from helps.abstract.abstractclass import Basic
from django.core.validators import MinValueValidator, MaxValueValidator
from helps.common.generic import Generichelps as ghelp
from user import models as MODELS_USER

# Create your models here.

def generate_unique_code():
    return ghelp().getUniqueCodePattern()

def upload_product_photo(instance, filename):
    return "product/photo/{uniquecode}uniquevalue{filename}".format(uniquecode=generate_unique_code(), filename=filename)

class Product(Basic):
    name  = models.CharField(max_length=200, blank=True, null=True)
    photo = models.ImageField(upload_to=upload_product_photo, blank=True, null=True)
    gallery = models.CharField(max_length=200, blank=True, null=True)
    weight = models.CharField(max_length=200, blank=True, null=True)
    quntity =  models.IntegerField(validators=[MinValueValidator(0)], default=1)
    costprice = models.FloatField(validators=[MinValueValidator(0)], blank=True, null=True)
    mrpprice = models.FloatField(validators=[MinValueValidator(0)], blank=True, null=True)

    created_by = models.ForeignKey(MODELS_USER.User, on_delete=models.SET_NULL, null=True, blank=True, related_name='product_created_by')
    updated_by = models.ForeignKey(MODELS_USER.User, on_delete=models.SET_NULL, null=True, blank=True, related_name='product_updated_by')

    def __str__(self):
        return f'{self.name} - {self.quntity}' 
