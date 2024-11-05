from rest_framework import serializers
from user import models

class Userserializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id', 'name', 'address', 'contact_no', 'email', 'username', 'password', 'role']

class Caategoryserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Permissioncategory
        fields = ['id', 'name']

class Permissionserializer(serializers.ModelSerializer):
    category = Caategoryserializer()
    class Meta:
        model = models.Permission
        fields = ['id', 'name', 'category']

class Roleserializer(serializers.ModelSerializer):
    permission = Permissionserializer(many=True)
    class Meta:
        model = models.Role
        fields = ['id', 'name', 'permission']