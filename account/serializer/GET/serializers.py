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

class Transectionserializer(serializers.ModelSerializer):
    income = Incomeserializer()
    expense = Expenseserializer()
    ordersummary = GET_SRLZER_ORDE.Ordersummaryserializer()
    class Meta:
        model = models.Transection
        fields = ['id', 'income', 'expense', 'ordersummary', 'reference', 'date', 'amount']

# class Transectionexpenseserializer(serializers.ModelSerializer):
#     income = Incomeserializer()
#     ordersummary = GET_SRLZER_ORDE.Ordersummaryserializer()
#     class Meta:
#         model = models.Transectionexpense
#         fields = ['id', 'expense', 'ordersummary', 'reference', 'date', 'amount']
