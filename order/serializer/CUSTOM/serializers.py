from rest_framework import serializers
from order import models
from user.serializer.CUSTOM import serializers as CUSTOM_SRLZER_USER
from zone.serializer.GET import serializers as GET_SRLZER_ZONE
from product.serializer.GET import serializers as GET_SRLZER_PROD

class Orderitemsserializer(serializers.ModelSerializer):
    product = GET_SRLZER_PROD.Productserializer(many=False)
    class Meta:
        model = models.Orderitems
        fields = ['id', 'product', 'order_quantity', 'unit_trade_price', 'unit_mrp']

class Ordersummaryserializer(serializers.ModelSerializer):
    user = CUSTOM_SRLZER_USER.Userserializer(many=False)
    deliveryzone = GET_SRLZER_ZONE.Deliveryzoneserializer(many=False)
    orderitems_ordersummary=Orderitemsserializer(many=True)
    class Meta:
        model = models.Ordersummary
        fields = ['id', 'user', 'date', 'invoice_no', 'deliveryzone', 'payment_mode', 'product_cost', 'coupon', 'discount', 'free_delivery', 'grand_total', 'total_profit', 'order_status', 'payment_status', 'orderitems_ordersummary', 'order_note']
