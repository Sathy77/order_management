from django.db import models
from helps.abstract.abstractclass import Basic
from django.core.validators import MinValueValidator, MaxValueValidator
from helps.common.generic import Generichelps as ghelp
from helps.choice import common as CHOICE
from user import models as MODELS_USER
from zone import models as MODELS_ZONE
from product import models as MODELS_PROD

# Create your models here.

class Ordersummary(Basic):
    user = models.ForeignKey(MODELS_USER.User, on_delete=models.CASCADE, related_name='ordersummary_user')
    date = models.DateField()
    invoice_no = models.CharField(max_length=100, blank=True, null=True, unique=True)
    deliveryzone = models.ForeignKey(MODELS_ZONE.Deliveryzone, on_delete=models.SET_NULL, blank=True, null=True, related_name='ordersummary_deliveryzone')
    payment_mode = models.CharField(max_length=25, choices=CHOICE.PAYMENT_MODE, default=CHOICE.PAYMENT_MODE[0][0], null=False)
    product_cost = models.FloatField(validators=[MinValueValidator(0)], blank=True, null=True)
    delivery_cost = models.FloatField(validators=[MinValueValidator(0)], blank=True, null=True)
    coupon = models.IntegerField(blank=True, null=True)
    discount = models.FloatField(validators=[MinValueValidator(0)], blank=True, null=True)
    free_delivery = models.BooleanField(default=False)
    grand_total = models.FloatField(validators=[MinValueValidator(0)], blank=True, null=True, default=0)
    total_profit = models.FloatField(blank=True, null=True)
    order_status = models.CharField(max_length=25, choices=CHOICE.ORDER_STATUS, default=CHOICE.ORDER_STATUS[0][1])
    payment_status = models.CharField(max_length=25, choices=CHOICE.PAYMENT_STATUS, default=CHOICE.PAYMENT_STATUS[0][1])
    order_note = models.CharField(max_length=300, blank=True, null=True)
    
    created_by = models.ForeignKey(MODELS_USER.User, on_delete=models.SET_NULL, null=True, blank=True, related_name='ordersummary_created_by')
    updated_by = models.ForeignKey(MODELS_USER.User, on_delete=models.SET_NULL, null=True, blank=True, related_name='ordersummary_updated_by')

    def __str__(self):
        return f'{self.id} - {self.date}' 
    
class Orderitems(Basic):
    ordersummary = models.ForeignKey(Ordersummary, on_delete=models.CASCADE, related_name='orderitems_ordersummary')
    product = models.ForeignKey(MODELS_PROD.Product, on_delete=models.CASCADE, related_name='orderitems_product')
    order_quantity = models.IntegerField()
    unit_trade_price = models.FloatField(validators=[MinValueValidator(0)], blank=True, null=True)
    unit_mrp = models.FloatField(validators=[MinValueValidator(0)], blank=True, null=True)

    # created_by = models.ForeignKey(MODELS_USER.User, on_delete=models.SET_NULL, null=True, blank=True, related_name='zone_created_by')
    # updated_by = models.ForeignKey(MODELS_USER.User, on_delete=models.SET_NULL, null=True, blank=True, related_name='zone_updated_by')

    def __str__(self):
        return f'{self.ordersummary} - {self.product}' 
    
class Storeorderid(Basic):
    last_order_id = models.IntegerField()

    # created_by = models.ForeignKey(MODELS_USER.User, on_delete=models.SET_NULL, null=True, blank=True, related_name='zone_created_by')
    # updated_by = models.ForeignKey(MODELS_USER.User, on_delete=models.SET_NULL, null=True, blank=True, related_name='zone_updated_by')

    def __str__(self):
        return f'{self.id} - {self.last_order_id}' 
    
