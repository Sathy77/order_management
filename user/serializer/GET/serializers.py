from rest_framework import serializers
from user import models


class Permissionserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Permission
        fields = ['id', 'name', 'serial']

class Permissioncategoryserializer(serializers.ModelSerializer):
    permissions=Permissionserializer(many=True)
    class Meta:
        model = models.Permissioncategory
        fields = ['id', 'name', 'permissions']
    
    def to_representation(self, instance):
        """
        Ensure permissions are always sorted by serial in ascending order.
        """
        representation = super().to_representation(instance)
        sorted_permissions = instance.permissions.all().order_by('serial')
        representation['permissions'] = Permissionserializer(sorted_permissions, many=True).data
        return representation

class Roleserializer(serializers.ModelSerializer):
    permission = Permissionserializer(many=True)
    class Meta:
        model = models.Role
        fields = ['id', 'name', 'permission']

class Userserializer(serializers.ModelSerializer):
    role=Roleserializer(many=True)
    class Meta:
        model = models.User
        fields = ['id', 'name', 'address', 'contact_no', 'email', 'username', 'password', 'role']


