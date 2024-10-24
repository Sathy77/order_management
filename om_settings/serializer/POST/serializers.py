from rest_framework import serializers
from om_settings import models

class Settingserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Settings
        fields = '__all__'
