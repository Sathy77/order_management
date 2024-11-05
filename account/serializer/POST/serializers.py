from rest_framework import serializers
from account import models

class Incomeserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Income
        fields = '__all__'

class Expenseserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Expense
        fields = '__all__'

class Transectionserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Transection
        fields = '__all__'

# class Transectionexpenseserializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Transectionexpense
#         fields = '__all__'

