from rest_framework import serializers
from account import models
from order.serializer.GET import serializers as GET_SRLZER_ORDE

class Incomeserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Income
        fields = ['id', 'title', 'balance']

class Expenseserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Expense
        fields = ['id', 'title', 'balance']

class Transectionincomeserializer(serializers.ModelSerializer):
    income = Incomeserializer()
    ordersummary = GET_SRLZER_ORDE.Ordersummaryserializer()
    class Meta:
        model = models.Transectionincome
        fields = ['id', 'income', 'ordersummary', 'reference', 'date', 'amount']

