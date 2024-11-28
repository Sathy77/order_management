from rest_framework import serializers
from product import models

class Productserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = ['id', 'name', 'type', 'capacity', 'photo', 'gallery', 'weight', 'quntity', 'costprice', 'mrpprice']

