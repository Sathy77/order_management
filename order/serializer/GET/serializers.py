from rest_framework import serializers
from order import models
from user.serializer.CUSTOM import serializers as CUSTOM_SRLZER_USER
from zone.serializer.GET import serializers as GET_SRLZER_ZONE
from product.serializer.GET import serializers as GET_SRLZER_PROD

class Ordersummaryserializer(serializers.ModelSerializer):
    user = CUSTOM_SRLZER_USER.Userserializer()
    deliveryzone = GET_SRLZER_ZONE.Deliveryzoneserializer()
    class Meta:
        model = models.Ordersummary
        fields = ['id', 'user', 'date', 'invoice_no', 'deliveryzone', 'payment_mode', 'product_cost', 'coupon', 'discount', 'free_delivery', 'grand_total', 'total_profit', 'order_status']


class Orderitemsserializer(serializers.ModelSerializer):
    ordersummary = Ordersummaryserializer()
    product = GET_SRLZER_PROD.Productserializer()
    class Meta:
        model = models.Orderitems
        fields = ['id', 'ordersummary', 'product', 'order_quantity', 'unit_trade_price', 'unit_mrp']

class Storeorderidserializer(serializers.ModelSerializer):
    class Meta:
        model = models.Storeorderid
        fields = '__all__'