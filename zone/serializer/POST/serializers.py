from rest_framework import serializers
from zone import models

class Deliveryzoneserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Deliveryzone
        fields = '__all__'
