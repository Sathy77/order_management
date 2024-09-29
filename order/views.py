from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from zone import models as MODELS_ZONE
from order import models as MODELS_ORDE
from user import models as MODELS_USER
from product import models as MODELS_PROD
from order.serializer.GET import serializers as GET_SRLZER_ORDE
from order.serializer.POST import serializers as POST_SRLZER_ORDE
# from payroll.serializer.POST import serializers as PSRLZER_PAYR
from helps.common.generic import Generichelps as ghelp
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from datetime import date
from rest_framework import status

# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getordersummary(request):
    filter_fields = [
        {'name': 'id', 'convert': None, 'replace':'id'},
        {'name': 'user', 'convert': None, 'replace':'user'},
        {'name': 'date', 'convert': None, 'replace':'date'},
        {'name': 'invoice_no', 'convert': None, 'replace':'invoice_no'},
        {'name': 'deliveryzone', 'convert': None, 'replace':'deliveryzone'},
        {'name': 'payment_mode', 'convert': None, 'replace':'payment_mode'},
        {'name': 'product_cost', 'convert': None, 'replace':'product_cost'},
        {'name': 'delivery_cost', 'convert': None, 'replace':'delivery_cost'},
        {'name': 'coupon', 'convert': None, 'replace':'coupon'},
        {'name': 'discount', 'convert': None, 'replace':'discount'},
        {'name': 'free_delivery', 'convert': 'bool', 'replace':'free_delivery'},
        {'name': 'grand_total', 'convert': None, 'replace':'grand_total'},
        {'name': 'total_profit', 'convert': None, 'replace':'total_profit'},
        {'name': 'order_status', 'convert': None, 'replace':'order_status'}
    ]
    ordersummarys = MODELS_ORDE.Ordersummary.objects.filter(**ghelp().KWARGS(request, filter_fields))

    column_accessor = request.GET.get('column_accessor')
    if column_accessor: ordersummarys = ordersummarys.order_by(column_accessor)
    
    total_count = ordersummarys.count()
    page = int(request.GET.get('page')) if request.GET.get('page') else 1
    page_size = int(request.GET.get('page_size')) if request.GET.get('page_size') else 10
    if page and page_size: ordersummarys=ordersummarys[(page-1)*page_size:page*page_size]

    ordersummaryserializers = GET_SRLZER_ORDE.Ordersummaryserializer(ordersummarys, many=True)
    return Response({'data': {
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'result': ordersummaryserializers.data
    }, 'message': [], 'status': 'success'}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getorderitems(request):
    filter_fields = [
        {'name': 'id', 'convert': None, 'replace':'id'},
        {'name': 'ordersummary', 'convert': None, 'replace':'ordersummary'},
        {'name': 'product', 'convert': None, 'replace':'product'},
        {'name': 'order_quantity', 'convert': None, 'replace':'order_quantity'},
        {'name': 'unit_trade_price', 'convert': None, 'replace':'unit_trade_price'},
        {'name': 'unit_mrp', 'convert': None, 'replace':'unit_mrp'},
    ]
    orderitems = MODELS_ORDE.Orderitems.objects.filter(**ghelp().KWARGS(request, filter_fields))

    column_accessor = request.GET.get('column_accessor')
    if column_accessor: orderitems = orderitems.order_by(column_accessor)
    
    total_count = orderitems.count()
    page = int(request.GET.get('page')) if request.GET.get('page') else 1
    page_size = int(request.GET.get('page_size')) if request.GET.get('page_size') else 10
    if page and page_size: orderitems=orderitems[(page-1)*page_size:page*page_size]

    orderitemsserializers = GET_SRLZER_ORDE.Orderitemsserializer(orderitems, many=True)
    return Response({'data': {
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'result': orderitemsserializers.data
    }, 'message': [], 'status': 'success'}, status=status.HTTP_200_OK)

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

        prepare_data={'product_cost': product_cost, 'grand_total': grand_total, 'total_profit': total_profit}
        ordersummeryid = ordersummery.first().id
        responsedata, responsemessage, responsesuccessflag, response_status = ghelp().updaterecord(
        classOBJ=MODELS_ORDE.Ordersummary, 
        Serializer=POST_SRLZER_ORDE.Ordersummaryserializer, 
        id=ordersummeryid, 
        data=prepare_data,
    )
        response_data = responsedata.data

    else:
        delevaryzoneid = request.data.get('deliveryzone')
        if delevaryzoneid:
            delevaryzone = MODELS_ZONE.Deliveryzone.objects.filter(id=delevaryzoneid)
            if delevaryzone.exists():
                deliverycost = delevaryzone.first().cost if delevaryzone.first().cost else 0
                todate = date.today()
                orderitems = MODELS_ORDE.Orderitems.objects.all().order_by('id').last()
                
                inv_first_serial = 100000
                inv_current_serial = inv_first_serial + orderitems.id if orderitems else inv_first_serial + 1
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
                responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().addtocolass(
                    classOBJ=MODELS_ORDE.Ordersummary, 
                    Serializer=POST_SRLZER_ORDE.Ordersummaryserializer, 
                    data=prepare_data, 
                    required_fields=required_fields,
                )
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


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# # @deco.get_permission(['get company info', 'all'])
# def addorderitems(request):
#     response_data = {}
#     response_message = []
#     response_successflag = 'error'
#     response_status = status.HTTP_400_BAD_REQUEST
#     requestdata = request.data.copy()
#     userid = request.user.id
    
#     delevaryzoneid = request.data.get('deliveryzone')
#     free_delivery = request.data.get('free_delivery')

#     if free_delivery:
#         if delevaryzoneid:
#             delevaryzone = MODELS_ZONE.Deliveryzone.objects.filter(id=delevaryzoneid)
#             if delevaryzone.exists():
#                 # delivery_Zone table theke delivery cost ana
#                 # deliverycost = delevaryzone.first().cost if delevaryzone.first().cost else 0
#                 todate = date.today()
#                 orderitems = MODELS_ORDE.Orderitems.objects.all().order_by('id').last()
                
#                 inv_first_serial = 100000
#                 inv_current_serial = inv_first_serial + orderitems.id if orderitems else 0 + 1
#                 invoice_no = f'INV{inv_current_serial}'

#                 deliverycost = 0
#                 grand_total = deliverycost
#                 total_profit = 0
#                 order_quantity = None
#                 product_cost = 0

#                 products = request.data.get('product')
#                 order_quantitys = request.data.get('order_quantity')
#                 unit_trade_prices = request.data.get('unit_trade_price')
#                 unit_mrps = request.data.get('unit_mrp')

#                 for index in range(len(products)):
#                     product_id = products[index]
#                     order_quantity = order_quantitys[index]
#                     unit_trade_price = unit_trade_prices[index]
#                     unit_mrp = unit_mrps[index]

#                     if unit_mrp:
#                         if order_quantity:
#                             product_cost = product_cost + unit_mrp*order_quantity

                            
#                             grand_total = grand_total + (unit_mrp*order_quantity)

#                             if unit_trade_price:
#                                 total_profit = total_profit + ((unit_mrp*order_quantity) - (unit_trade_price*order_quantity))

#                 user = MODELS_USER.User.objects.get(id=userid)
#                 prepare_data={'user': user.id, 'date': todate, 'invoice_no': invoice_no, 'deliveryzone': requestdata['deliveryzone'], 'product_cost': product_cost, 'delivery_cost': deliverycost, 'grand_total': grand_total, 'total_profit': total_profit}
#                 # if userid: extra_fields.update({'created_by': userid, 'updated_by': userid})
#                 required_fields = ['deliveryzone']

#                 responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().addtocolass(
#                     classOBJ=MODELS_ORDE.Ordersummary, 
#                     Serializer=POST_SRLZER_ORDE.Ordersummaryserializer, 
#                     data=prepare_data, 
#                     required_fields=required_fields,
#                 )
#                 response_data = responsedata.data
#                 ordersummery = response_data['id']

#                 for index in range(len(products)):
#                     product_id = products[index]
#                     order_quantity = order_quantitys[index]
#                     unit_trade_price = unit_trade_prices[index]
#                     unit_mrp = unit_mrps[index]

#                     userid = request.user.id
#                     # extra_fields = {}
#                     ordersummary = response_data['id']
#                     prepare_data={'ordersummary': ordersummery, 'product': product_id, 'order_quantity': order_quantity, 'unit_trade_price': unit_trade_price, 'unit_mrp': unit_mrp}
#                     # if userid: extra_fields.update({'created_by': userid, 'updated_by': userid})
#                     required_fields = ['ordersummary', 'product', 'order_quantity', 'unit_trade_price', 'unit_mrp']
                
#                     responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().addtocolass(
#                         classOBJ=MODELS_ORDE.Orderitems, 
#                         Serializer=POST_SRLZER_ORDE.Orderitemsserializer, 
#                         data=prepare_data, 
#                         # extra_fields=extra_fields,
#                         required_fields=required_fields,
#                     )
#                     response_message = responsemessage
#                     response_successflag = responsesuccessflag
#                     response_data = responsedata.data
#                     response_status = responsestatus

#     else:
#         if delevaryzoneid:
#             delevaryzone = MODELS_ZONE.Deliveryzone.objects.filter(id=delevaryzoneid)
#             if delevaryzone.exists():
#                 deliverycost = delevaryzone.first().cost if delevaryzone.first().cost else 0
#                 todate = date.today()
#                 orderitems = MODELS_ORDE.Orderitems.objects.all().order_by('id').last()
                
#                 inv_first_serial = 100000
#                 inv_current_serial = inv_first_serial + orderitems.id if orderitems else 0 + 1
#                 invoice_no = f'INV{inv_current_serial}'

#                 grand_total = deliverycost
#                 total_profit = 0
#                 order_quantity = None
#                 product_cost = 0

#                 products = request.data.get('product')
#                 order_quantitys = request.data.get('order_quantity')
#                 unit_trade_prices = request.data.get('unit_trade_price')
#                 unit_mrps = request.data.get('unit_mrp')

#                 for index in range(len(products)):
#                     product_id = products[index]
#                     order_quantity = order_quantitys[index]
#                     unit_trade_price = unit_trade_prices[index]
#                     unit_mrp = unit_mrps[index]

#                     if unit_mrp:
#                         if order_quantity:
#                             product_cost = product_cost + unit_mrp*order_quantity

#                             if deliverycost:
#                                 grand_total = grand_total + (unit_mrp*order_quantity)

#                             if unit_trade_price:
#                                 total_profit = total_profit + ((unit_mrp*order_quantity) - (unit_trade_price*order_quantity))

#                 user = MODELS_USER.User.objects.get(id=userid)
#                 prepare_data={'user': user.id, 'date': todate, 'invoice_no': invoice_no, 'deliveryzone': requestdata['deliveryzone'], 'product_cost': product_cost, 'delivery_cost': deliverycost, 'grand_total': grand_total, 'total_profit': total_profit}
#                 # if userid: extra_fields.update({'created_by': userid, 'updated_by': userid})
#                 required_fields = ['deliveryzone']

#                 responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().addtocolass(
#                     classOBJ=MODELS_ORDE.Ordersummary, 
#                     Serializer=POST_SRLZER_ORDE.Ordersummaryserializer, 
#                     data=prepare_data, 
#                     required_fields=required_fields,
#                 )
#                 response_data = responsedata.data
#                 ordersummery = response_data['id']

#                 for index in range(len(products)):
#                     product_id = products[index]
#                     order_quantity = order_quantitys[index]
#                     unit_trade_price = unit_trade_prices[index]
#                     unit_mrp = unit_mrps[index]

#                     userid = request.user.id
#                     # extra_fields = {}
#                     ordersummary = response_data['id']
#                     prepare_data={'ordersummary': ordersummery, 'product': product_id, 'order_quantity': order_quantity, 'unit_trade_price': unit_trade_price, 'unit_mrp': unit_mrp}
#                     # if userid: extra_fields.update({'created_by': userid, 'updated_by': userid})
#                     required_fields = ['ordersummary', 'product', 'order_quantity', 'unit_trade_price', 'unit_mrp']
                
#                     responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().addtocolass(
#                         classOBJ=MODELS_ORDE.Orderitems, 
#                         Serializer=POST_SRLZER_ORDE.Orderitemsserializer, 
#                         data=prepare_data, 
#                         # extra_fields=extra_fields,
#                         required_fields=required_fields,
#                     )
#                     response_message = responsemessage
#                     response_successflag = responsesuccessflag
#                     response_data = responsedata.data
#                     response_status = responsestatus
    

#     return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)
