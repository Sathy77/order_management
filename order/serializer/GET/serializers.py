from rest_framework import serializers
from order import models

class Ordersummaryserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Ordersummary
        fields = ['id', 'user', 'date', 'invoice_no', 'deliveryzone', 'payment_mode', 'product_cost', 'coupon', 'discount', 'free_delivery', 'grand_total', 'total_profit', 'order_status']


class Orderitemsserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Orderitems
        fields = ['id', 'ordersummary', 'product', 'order_quantity', 'unit_trade_price', 'unit_mrp']
