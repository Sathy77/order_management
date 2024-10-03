from django.db import models
from helps.abstract.abstractclass import Basic
from django.core.validators import MinValueValidator, MaxValueValidator
from helps.common.generic import Generichelps as ghelp
from user import models as MODELS_USER
from order import models as MODELS_ORDE

# Create your models here.
class Income(Basic):
    title = models.CharField(max_length=200)
    balance = models.FloatField(validators=[MinValueValidator(0)], default=0)

    created_by = models.ForeignKey(MODELS_USER.User, on_delete=models.SET_NULL, null=True, blank=True, related_name='income_created_by')
    updated_by = models.ForeignKey(MODELS_USER.User, on_delete=models.SET_NULL, null=True, blank=True, related_name='income_updated_by')

    def __str__(self):
        return f'{self.id} - {self.title}' 
    
class Expense(Basic):
    title = models.CharField(max_length=200)
    balance = models.FloatField(validators=[MinValueValidator(0)], default=0)

    created_by = models.ForeignKey(MODELS_USER.User, on_delete=models.SET_NULL, null=True, blank=True, related_name='expense_created_by')
    updated_by = models.ForeignKey(MODELS_USER.User, on_delete=models.SET_NULL, null=True, blank=True, related_name='expense_updated_by')

    def __str__(self):
        return f'{self.id} - {self.title}' 
    
class Transectionincome(Basic):
    income = models.ForeignKey(Income, on_delete=models.CASCADE, related_name='transectionincome_income')
    ordersummary = models.ForeignKey(MODELS_ORDE.Ordersummary, on_delete=models.SET_NULL, null=True, blank=True, related_name='transectionincome_ordersummary')
    reference = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField()
    amount = models.FloatField(validators=[MinValueValidator(0)], blank=True, null=True)

    def __str__(self):
        return f'{self.id} - {self.date}' 
    
class Transectionexpense(Basic):
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name='transectionexpense_expense')
    ordersummary = models.ForeignKey(MODELS_ORDE.Ordersummary, on_delete=models.SET_NULL, null=True, blank=True, related_name='transectionexpense_ordersummary')
    reference = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField()
    amount = models.FloatField(validators=[MinValueValidator(0)], blank=True, null=True)

    def __str__(self):
        return f'{self.id} - {self.date}' 