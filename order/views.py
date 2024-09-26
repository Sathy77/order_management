from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from zone import models as MODELS_ZONE
from order import models as MODELS_ORDE
from user import models as MODELS_USER
from product import models as MODELS_PROD
from order.serializer.GET import serializers as GET_SRLZER_ZONE
from order.serializer.POST import serializers as POST_SRLZER_ORDE
# from payroll.serializer.POST import serializers as PSRLZER_PAYR
from helps.common.generic import Generichelps as ghelp
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from datetime import date
from rest_framework import status
import copy

# Create your views here.

@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['get company info', 'all'])
def addorderitems(request):
    response_data = {}
    response_message = []
    response_successflag = 'error'
    response_status = status.HTTP_400_BAD_REQUEST
    requestdata = request.data.copy()
    userid = request.user.id
    user = MODELS_USER.User.objects.get(id=userid)

    # Retrieve all Ordersummary instances for this user
    ordersummery = MODELS_ORDE.Ordersummary.objects.filter(user=user)
    if ordersummery.exists():
        unit_mrp = request.data.get('unit_mrp')
        if unit_mrp:
            order_quantity = request.data.get('order_quantity')
            if order_quantity:
                product_cost = ordersummery.first().product_cost
                product_cost = product_cost + (unit_mrp*order_quantity)

                grand_total = ordersummery.first().grand_total
                grand_total = grand_total + (unit_mrp*order_quantity)

                unit_trade_price = request.data.get('unit_trade_price')
                if unit_trade_price:
                    total_profit = ordersummery.first().total_profit
                    total_profit = total_profit + ((unit_mrp*order_quantity) - (unit_trade_price*order_quantity))

        _instance = MODELS_ORDE.Ordersummary.objects.get(id=ordersummery.first().id)
        _instance.product_cost = product_cost
        _instance.grand_total = grand_total
        _instance.total_profit = total_profit
        _instance.save() 

    else:
        delevaryzoneid = request.data.get('deliveryzone')
        if delevaryzoneid:
            delevaryzone = MODELS_ZONE.Deliveryzone.objects.filter(id=delevaryzoneid)
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
                        product_cost = unit_mrp*order_quantity

                        if deliverycost:
                            grand_total = product_cost + deliverycost

                        unit_trade_price = request.data.get('unit_trade_price')
                        if unit_trade_price:
                            total_profit = product_cost - unit_trade_price*order_quantity
                
                user = MODELS_USER.User.objects.get(id=userid)
                prepare_data={'user': user.id, 'date': todate, 'invoice_no': invoice_no, 'deliveryzone': requestdata['deliveryzone'], 'product_cost': product_cost, 'delivery_cost': deliverycost, 'grand_total': grand_total, 'total_profit': total_profit}
                # if userid: extra_fields.update({'created_by': userid, 'updated_by': userid})
                required_fields = ['deliveryzone']

                # _instance = MODELS_ORDE.Ordersummary()
                # _instance.user = MODELS_USER.User.objects.get(id=userid)
                # _instance.date = todate
                # _instance.invoice_no = invoice_no
                # _instance.deliveryzone = delevaryzone.first()
                # # _instance.payment_mode = request.data.get('payment_mode')
                # if unit_mrp: _instance.product_cost = product_cost
                # _instance.delivery_cost = deliverycost
                # # _instance.coupon = None
                # if grand_total: _instance.grand_total = grand_total
                # if total_profit: _instance.total_profit = total_profit
                # _instance.save()
                responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().addtocolass(
                    classOBJ=MODELS_ORDE.Ordersummary, 
                    Serializer=POST_SRLZER_ORDE.Ordersummaryserializer, 
                    data=prepare_data, 
                    required_fields=required_fields,
                )
                print(responsesuccessflag)
                response_data = responsedata.data

    userid = request.user.id
    # extra_fields = {}
    ordersummary = response_data['id']
    prepare_data={'ordersummary': ordersummary, 'product': requestdata['product'], 'order_quantity': requestdata['order_quantity'], 'unit_trade_price': requestdata['unit_trade_price'], 'unit_mrp': requestdata['unit_mrp']}
    # if userid: extra_fields.update({'created_by': userid, 'updated_by': userid})
    required_fields = ['ordersummary', 'product', 'order_quantity', 'unit_trade_price', 'unit_mrp']
  
    responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().addtocolass(
        classOBJ=MODELS_ORDE.Orderitems, 
        Serializer=POST_SRLZER_ORDE.Orderitemsserializer, 
        data=prepare_data, 
        # extra_fields=extra_fields,
        required_fields=required_fields,
    )
    response_message = responsemessage
    response_successflag = responsesuccessflag
    response_data = responsedata.data.copy()
    response_status = responsestatus
    

    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)
