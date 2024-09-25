from rest_framework import serializers
from order import models

class Ordersummaryserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Ordersummary
        fields = '__all__'

class Orderitemsserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Orderitems
        fields = '__all__'
