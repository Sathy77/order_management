from rest_framework import serializers
from user import models

class Userserializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = '__all__'

class Permissionserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Permission
        fields = '__all__'

class Roleserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Role
        fields = '__all__'
