from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from zone import models as MODELS_ZONE
from order import models as MODELS_ORDE
from user import models as MODELS_USER
from product import models as MODELS_PROD
from zone.serializer.GET import serializers as GET_SRLZER_ZONE
from zone.serializer.POST import serializers as POST_SRLZER_ZONE
# from payroll.serializer.POST import serializers as PSRLZER_PAYR
from helps.common.generic import Generichelps as ghelp
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from datetime import date

# Create your views here.

@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['get company info', 'all'])
def addorderitems(request):
    requestdata = request.data.copy()
    userid = request.user.id
    # ordersummery=MODELS_ORDE.Ordersummary.objects.filter(id=request.data.get('ordersummary'))
    # print("=======================", ordersummery.exists())
    delevaryzoneid = request.data.get('deliveryzone')
    if delevaryzoneid:
        delevaryzone = MODELS_ZONE.Deliveryzone.objects.filter(id=delevaryzoneid)
        # print("--------------------",delevaryzone)
        # delevaryzone_= dict(delevaryzone)
        # print("------gggggggggggg--------------",delevaryzone_)
        if delevaryzone.exists():
            deliverycost = delevaryzone.first().cost if delevaryzone.first().cost else 0
            todate = date.today()
            orderitems = MODELS_ORDE.Orderitems.objects.all().order_by('id').last()
            
            inv_first_serial = 100000
            inv_current_serial = inv_first_serial + orderitems.id if orderitems else 0 + 1
            invoice_no = f'INV{inv_current_serial}'

            grand_total = None
            total_profit = None
            order_quantity = None
            unit_mrp = request.data.get('unit_mrp')
            if unit_mrp:
                order_quantity = request.data.get('order_quantity')
                if order_quantity:
                    grand_total = unit_mrp*order_quantity

                    unit_trade_price = request.data.get('unit_trade_price')
                    if unit_trade_price:
                        total_profit = grand_total - unit_trade_price*order_quantity


            _instance = MODELS_ORDE.Ordersummary()
            _instance.user = MODELS_USER.User.objects.get(id=userid)
            _instance.date = todate
            _instance.invoice_no = invoice_no
            _instance.deliveryzone = delevaryzone.first()
            _instance.payment_mode = request.data.get('payment_mode')
            if unit_mrp: _instance.product_cost = unit_mrp
            _instance.delivery_cost = deliverycost
            # _instance.coupon = None
            if grand_total: _instance.grand_total = grand_total
            if total_profit: _instance.total_profit = total_profit
            _instance.save()

            productid = request.data.get('product')
            product = MODELS_PROD.Product.objects.filter(id=productid)

            instance = MODELS_ORDE.Orderitems()
            instance.ordersummary = _instance
            instance.product = product.first()
            instance.order_quantity = order_quantity
            instance.unit_trade_price = unit_trade_price
            instance.unit_mrp = unit_mrp
            instance.save()

            

    return Response('ok')
