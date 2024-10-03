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

class Transectionincomeserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Transectionincome
        fields = '__all__'

