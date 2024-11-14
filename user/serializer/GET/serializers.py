from rest_framework import serializers
from user import models

class Roleserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Role
        fields = ['id', 'name']

class Userserializer(serializers.ModelSerializer):
    role=Roleserializer(many=True)
    class Meta:
        model = models.User
        fields = ['id', 'name', 'address', 'contact_no', 'email', 'username', 'password', 'role']


class Permissionserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Permission
        fields = ['id', 'name']

class Permissioncategoryserializer(serializers.ModelSerializer):
    permissions=Permissionserializer(many=True)
    class Meta:
        model = models.Permissioncategory
        fields = ['id', 'name', 'permissions']


