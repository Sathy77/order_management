from rest_framework import serializers
from order import models
from user.serializer.CUSTOM import serializers as CUSTOM_SRLZER_USER
from zone.serializer.GET import serializers as GET_SRLZER_ZONE
from product.serializer.GET import serializers as GET_SRLZER_PROD
# from account import models as MODELS_ACCO
from django.db.models import Sum

class Orderitemsserializer(serializers.ModelSerializer):
    product = GET_SRLZER_PROD.Productserializer(many=False)
    class Meta:
        model = models.Orderitems
        fields = ['id', 'product', 'order_quantity', 'unit_trade_price', 'unit_mrp']

class Ordersummaryserializer(serializers.ModelSerializer):
    user = CUSTOM_SRLZER_USER.Userserializer(many=False)
    deliveryzone = GET_SRLZER_ZONE.Deliveryzoneserializer(many=False)
    orderitems_ordersummary=Orderitemsserializer(many=True)
    due_amount=serializers.SerializerMethodField('calculate_amount')

    def calculate_amount(self, instance):
        """
        Calculate the due amount for an order.
        """
        if instance.grand_total is not None:
            total_paid = instance.transection_ordersummary.aggregate(Sum('amount'))['amount__sum'] or 0
            return instance.grand_total - total_paid
        
        return 0.0  # Default value if grand_total is None
    class Meta:
        model = models.Ordersummary
        fields = ['id', 'user', 'date', 'invoice_no', 'deliveryzone', 'payment_mode', 'product_cost', 'coupon', 'discount', 'free_delivery', 'grand_total', 'total_profit', 'order_status', 'is_combo', 'combo_name', 'combo_quantity', 'payment_status', 'orderitems_ordersummary', 'order_note', 'due_amount']
