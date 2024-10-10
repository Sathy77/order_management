from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from zone import models as MODELS_ZONE
from order import models as MODELS_ORDE
from user import models as MODELS_USER
from product import models as MODELS_PROD
from order.serializer.GET import serializers as GET_SRLZER_ORDE
from order.serializer.POST import serializers as POST_SRLZER_ORDE
# from payroll.serializer.POST import serializers as PSRLZER_PAYR
from user.serializer.POST import serializers as POST_SRLZER_USER
from product.serializer.POST import serializers as POST_SRLZER_PROD
from django.contrib.auth.hashers import make_password
from helps.common.generic import Generichelps as ghelp
from helps.choice import common as CHOICE
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
#     user = MODELS_USER.User.objects.get(id=userid)

#     # Retrieve all Ordersummary instances for this user
#     ordersummery = MODELS_ORDE.Ordersummary.objects.filter(user=user)
#     if ordersummery.exists():
#         unit_mrp = request.data.get('unit_mrp')
#         if unit_mrp:
#             order_quantity = request.data.get('order_quantity')
#             if order_quantity:
#                 product_cost = ordersummery.first().product_cost
#                 product_cost = product_cost + (unit_mrp*order_quantity)

#                 grand_total = ordersummery.first().grand_total
#                 grand_total = grand_total + (unit_mrp*order_quantity)

#                 unit_trade_price = request.data.get('unit_trade_price')
#                 if unit_trade_price:
#                     total_profit = ordersummery.first().total_profit
#                     total_profit = total_profit + ((unit_mrp*order_quantity) - (unit_trade_price*order_quantity))

#         prepare_data={'product_cost': product_cost, 'grand_total': grand_total, 'total_profit': total_profit}
#         ordersummeryid = ordersummery.first().id
#         responsedata, responsemessage, responsesuccessflag, response_status = ghelp().updaterecord(
#         classOBJ=MODELS_ORDE.Ordersummary, 
#         Serializer=POST_SRLZER_ORDE.Ordersummaryserializer, 
#         id=ordersummeryid, 
#         data=prepare_data,
#     )
#         response_data = responsedata.data

#     else:
#         delevaryzoneid = request.data.get('deliveryzone')
#         if delevaryzoneid:
#             delevaryzone = MODELS_ZONE.Deliveryzone.objects.filter(id=delevaryzoneid)
#             if delevaryzone.exists():
#                 deliverycost = delevaryzone.first().cost if delevaryzone.first().cost else 0
#                 todate = date.today()
#                 orderitems = MODELS_ORDE.Orderitems.objects.all().order_by('id').last()
                
#                 inv_first_serial = 100000
#                 inv_current_serial = inv_first_serial + orderitems.id if orderitems else inv_first_serial + 1
#                 invoice_no = f'INV{inv_current_serial}'

#                 grand_total = None
#                 total_profit = None
#                 order_quantity = None
#                 unit_mrp = request.data.get('unit_mrp')
#                 if unit_mrp:
#                     order_quantity = request.data.get('order_quantity')
#                     if order_quantity:
#                         product_cost = unit_mrp*order_quantity

#                         if deliverycost:
#                             grand_total = product_cost + deliverycost

#                         unit_trade_price = request.data.get('unit_trade_price')
#                         if unit_trade_price:
#                             total_profit = product_cost - unit_trade_price*order_quantity
                
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

#     userid = request.user.id
#     # extra_fields = {}
#     ordersummary = response_data['id']
#     prepare_data={'ordersummary': ordersummary, 'product': requestdata['product'], 'order_quantity': requestdata['order_quantity'], 'unit_trade_price': requestdata['unit_trade_price'], 'unit_mrp': requestdata['unit_mrp']}
#     # if userid: extra_fields.update({'created_by': userid, 'updated_by': userid})
#     required_fields = ['ordersummary', 'product', 'order_quantity', 'unit_trade_price', 'unit_mrp']
  
#     responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().addtocolass(
#         classOBJ=MODELS_ORDE.Orderitems, 
#         Serializer=POST_SRLZER_ORDE.Orderitemsserializer, 
#         data=prepare_data, 
#         # extra_fields=extra_fields,
#         required_fields=required_fields,
#     )
#     response_message = responsemessage
#     response_successflag = responsesuccessflag
#     response_data = responsedata.data.copy()
#     response_status = responsestatus

#     return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)



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
    free_delivery = True
    contact_no = request.data.get('contact_no')
    if contact_no:
        delevaryzoneid = requestdata.get('deliveryzone')
        deliverycost = 0
        if delevaryzoneid:
            delevaryzone = MODELS_ZONE.Deliveryzone.objects.filter(id=delevaryzoneid)
            if delevaryzone.exists():
                if not requestdata.get('free_delivery'):
                    deliverycost = delevaryzone.first().cost if delevaryzone.first().cost else 0
                    free_delivery = False
                
                todate = date.today()
                payment_mode = requestdata.get('payment_mode') ## frontend theke valu dile recive korbe na dile none pathabe
                
                product_costs = requestdata.get('product_cost')
                try: product_costs += 0
                except: response_message.append('product_costs should be type of float!')
                grand_totals = requestdata.get('grand_total')
                try: grand_totals += 0
                except: response_message.append('grand_totals should be type of float!')
                discounts = requestdata.get('discount')
                try: discounts += 0
                except: response_message.append('discounts should be type of float!')

                ##create customer
                if not response_message:
                    response = ghelp().purifyProducts(MODELS_PROD.Product, requestdata)
                    if not response['message']:
                        user = MODELS_USER.User.objects.filter(contact_no=contact_no) 
                        if not user.exists():
                            allowed_fields = ['name', 'address', 'contact_no']
                            extra_fields = {'username': contact_no, 'password': make_password(f'PASS{contact_no}'), 'created_by': userid, 'updated_by': userid}
                            required_fields = ['name', 'address', 'contact_no']
                            fields_regex = [{'field': 'contact_no', 'type': 'phonenumber'}]
                            unique_fields=['contact_no']
                            responsedata, responsemessage, responsesuccessflag, _ = ghelp().addtocolass(
                                classOBJ=MODELS_USER.User,
                                Serializer=POST_SRLZER_USER.Userserializer,
                                data=requestdata,
                                allowed_fields=allowed_fields,
                                required_fields=required_fields,
                                unique_fields=unique_fields,
                                extra_fields=extra_fields,
                                fields_regex=fields_regex
                            )
                            if responsesuccessflag == 'success': user = responsedata.instance
                            elif responsesuccessflag == 'error': response_message.extend(responsemessage)
                        else: user = user.first()

                        if not response_message:
                            discount = 0
                            product_cost, grand_total, total_profit = ghelp().calculateProductCalculation(response['products'], discount, deliverycost)

                            if product_cost != product_costs: response_message.append(f'total calculated product_cost is not matching, calculated({product_cost}) != provided({product_costs})')
                            if grand_total != grand_totals: response_message.append(f'calculated grand_total is not matching, calculated({grand_total}) != provided({grand_totals})')
                            if discount != discounts: response_message.append(f'calculated discount is not matching, calculated({discount}) != provided({discounts})')
                            
                            ##create ordersummary
                            if not response_message:
                                #invoice auto create
                                orderitems = MODELS_ORDE.Orderitems.objects.all().order_by('id').last()
                                inv_first_serial = 100000
                                inv_current_serial = inv_first_serial + orderitems.id if orderitems else inv_first_serial + 1
                                invoice_no = f'INV{inv_current_serial}'

                                prepare_data={
                                    'user': user.id,
                                    'date': todate,
                                    'invoice_no': invoice_no,
                                    'deliveryzone': delevaryzoneid,
                                    'product_cost': product_cost,
                                    'delivery_cost': deliverycost,
                                    'free_delivery': free_delivery,
                                    'grand_total': grand_total,
                                    'total_profit': total_profit,
                                    'discount': discount,
                                    'payment_mode': payment_mode
                                }
                                
                                required_fields = ['deliveryzone']
                                responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().addtocolass(
                                    classOBJ=MODELS_ORDE.Ordersummary,
                                    Serializer=POST_SRLZER_ORDE.Ordersummaryserializer,
                                    data=prepare_data,
                                    required_fields=required_fields
                                )
                                #create orderitems and update product quantity
                                if responsesuccessflag == 'success':
                                    for productkey in response['products'].keys():
                                        product = response['products'][productkey]['product']
                                        prepare_data={
                                            'ordersummary': responsedata.data['id'],
                                            'product': productkey,
                                            'order_quantity': response['products'][productkey]['quantity'],
                                            'unit_trade_price': product.first().costprice,
                                            'unit_mrp': product.first().mrpprice
                                        }
                                        #create orderitems
                                        ghelp().addtocolass(classOBJ=MODELS_ORDE.Orderitems, Serializer=POST_SRLZER_ORDE.Orderitemsserializer, data=prepare_data)
                                        response_successflag = responsesuccessflag
                                        response_data = responsedata.data
                                        response_status = responsestatus

                                        #Update product quantity
                                        if responsesuccessflag == 'success':
                                            order_quantity = response['products'][productkey]['quantity']
                                            product = MODELS_PROD.Product.objects.filter(id=productkey)
                                            quantity = product.first().quntity
                                            quantity -= order_quantity
                                            prepare_data={'quntity': quantity}
                                            ghelp().updaterecord(classOBJ=MODELS_PROD.Product, Serializer=POST_SRLZER_PROD.Productserializer, id=productkey,data=prepare_data)

                                elif responsesuccessflag == 'error': response_message.extend(responsemessage)
                    else: response_message.extend(response['message'])
            else: response_message.append('delivary zone id is invalid!')
        else: response_message.append('delivary zone is required!')
    else: response_message.append('please provide contact number!')
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)




@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def updateordersummarystatus(request, ordersummaryid=None):
    response_data = {}
    response_message = []
    response_successflag = 'error'
    response_status = status.HTTP_400_BAD_REQUEST
    requestdata = request.data.copy()
    order_status = requestdata.get('order_status')
    if order_status:
        freez_update = [{'order_status': [CHOICE.ORDER_STATUS[3][1], CHOICE.ORDER_STATUS[4][1], CHOICE.ORDER_STATUS[5][1]]}]
        response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
            classOBJ=MODELS_ORDE.Ordersummary,
            Serializer=POST_SRLZER_ORDE.Ordersummaryserializer,
            id=ordersummaryid,
            data = {'order_status': order_status},
            freez_update = freez_update
        )
        # Ensure that response_data is serialized
        if isinstance(response_data, POST_SRLZER_ORDE.Ordersummaryserializer):
            response_data = response_data.data  # Access the .data attribute
        
        if response_successflag == "success" and (order_status == "Cancelled" or order_status == "Returned" ):
            orderitems = MODELS_ORDE.Orderitems.objects.filter(ordersummary=ordersummaryid)
            for orderitem in orderitems:
                product = orderitem.product
                productid = product.id
                order_quantity = orderitem.order_quantity
                product = MODELS_PROD.Product.objects.filter(id=productid)
                quantity = product.first().quntity
                quantity += order_quantity
                prepare_data={'quntity': quantity}
                ghelp().updaterecord(classOBJ=MODELS_PROD.Product, Serializer=POST_SRLZER_PROD.Productserializer, id=productid,data=prepare_data)

    else: response_message.append('order_status is required!')
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)







###আমার 
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
#     user = MODELS_USER.User.objects.get(id=userid)
#     print("jjjjjjjjjjjjjjjjjjjjj",requestdata)

#     contact_no = request.data.get('contact_no')
#     user = MODELS_USER.User.objects.filter(contact_no=contact_no) 
#     if not user.exists():
#         name = request.data.get('name')
#         address = request.data.get('address')
#         password = f'PASS{contact_no}'
#         username = contact_no

#         requestdata = request.data.copy()
#         userid = request.user.id
#         extra_fields = {}
#         if userid: extra_fields.update({'created_by': request.user.id, 'updated_by': request.user.id})
#         prepare_data={'name': name, 'contact_no': contact_no, 'address': address, 'username': username, 'password': password}
#         required_fields = ['name', 'address', 'contact_no']
#         if 'password' in requestdata: requestdata['password'] = make_password(requestdata['password'])
#         responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().addtocolass(
#             classOBJ=MODELS_USER.User, 
#             Serializer=POST_SRLZER_USER.Userserializer, 
#             data=prepare_data, 
#             unique_fields=['contact_no'], 
#             extra_fields=extra_fields, 
#             required_fields=required_fields
#     )
#         response_data = responsedata.data
#         user = response_data['id']
        

#     else:
#         user = user.first().id

#     # Retrieve all Ordersummary instances for this user
   
#     delevaryzoneid = request.data.get('deliveryzone')
#     deliverycost = 0
#     if delevaryzoneid:
#         delevaryzone = MODELS_ZONE.Deliveryzone.objects.filter(id=delevaryzoneid)
#         if delevaryzone.exists():
#             if not request.data.get('free_delivery'):
#                 deliverycost = delevaryzone.first().cost if delevaryzone.first().cost else 0
#             todate = date.today()
#             payment_mode = request.data.get('payment_mode') ## frontend theke valu dile recive korbe na dile none pathabe
#             # payment_mode = request.data['payment_mode'] ## frontend theke valu dile recive korbe na dile error dibe
            
#             # if 'payment_mode' in requestdata:
#             #     payment_mode = request.data.get('payment_mode')
#             # else :
#             #     payment_mode = CHOICE.PAYMENT_MODE[0][0]

#             product_costs = request.data.get('product_cost')
#             grand_totals = request.data.get('grand_total')
#             discounts = request.data.get('discount')

#             product_cost = 0
#             grand_total = deliverycost
#             total_profit = 0
#             discount = 0
            
#             orderitems = MODELS_ORDE.Orderitems.objects.all().order_by('id').last()
#             inv_first_serial = 100000
#             inv_current_serial = inv_first_serial + orderitems.id if orderitems else inv_first_serial + 1
#             invoice_no = f'INV{inv_current_serial}'
            
# # Retrieve all Orderiteams instances for this user
#             products = request.data.get('products')
#             # order_quantitys = request.data.get('order_quantity')
#             unit_trade_price = None
#             unit_mrp = None

#             for index in range(len(products)):
#                 product = products[index]
#                 if product:
#                     productid = product.get('id')
#                     order_quantity = product.get('order_quantity')
#                     if productid:
#                         product = MODELS_PROD.Product.objects.filter(id=productid)
#                         if product.exists():
#                             unit_trade_price = product.first().costprice if product.first().costprice else 0
#                             unit_mrp = product.first().mrpprice if product.first().mrpprice else 0

#                         if unit_mrp:
#                             if order_quantity <= product.first().quntity:
#                                 product_cost = product_cost + (unit_mrp*order_quantity)
#                                 grand_total = grand_total + ((unit_mrp*order_quantity) - discount)
#                                 if unit_trade_price:
#                                     total_profit = total_profit + (((unit_mrp*order_quantity) - discount) - (unit_trade_price*order_quantity))
#                             else:
#                                 response_message = "Not enough in stock"
#                                 return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

#                             # userid = request.user.id
#                             # extra_fields = {}
#             prepare_data={}
#             if product_cost == product_costs:
#                 if grand_total == grand_totals:
#                     if discount == discounts:
#                         prepare_data={'user': user, 'date': todate, 'invoice_no': invoice_no, 'deliveryzone': delevaryzoneid, 'product_cost': product_cost, 'delivery_cost': deliverycost, 'grand_total': grand_total, 'total_profit': total_profit, 'discount': discount, 'payment_mode': payment_mode}
                    
#                     else:
#                         response_message = "Invalid discount"
#                         return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)
#                 else:
#                     response_message = "Invalid grand total"
#                     return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)  
#             else:
#                 response_message = "Invalid product cost"
#                 return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

            
#             # if userid: extra_fields.update({'created_by': userid, 'updated_by': userid})
#             required_fields = ['deliveryzone']
#             responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().addtocolass(
#                 classOBJ=MODELS_ORDE.Ordersummary, 
#                 Serializer=POST_SRLZER_ORDE.Ordersummaryserializer, 
#                 data=prepare_data, 
#                 required_fields=required_fields,
#             )
#             summary_response_data = responsedata.data

#             for index in range(len(products)):
#                 product = products[index]
#                 if product:
#                     productid = product.get('id')
#                     order_quantity = product.get('order_quantity')
#                     if productid:
#                         product = MODELS_PROD.Product.objects.filter(id=productid)
#                         if product.exists():
#                             unit_trade_price = product.first().costprice if product.first().costprice else 0
#                             unit_mrp = product.first().mrpprice if product.first().mrpprice else 0
#                             ordersummary = summary_response_data['id']
#                             prepare_data={'ordersummary': ordersummary, 'product': productid, 'order_quantity': order_quantity, 'unit_trade_price': unit_trade_price, 'unit_mrp': unit_mrp}
#                             # if userid: extra_fields.update({'created_by': userid, 'updated_by': userid})
#                             required_fields = ['ordersummary', 'product', 'order_quantity', 'unit_trade_price', 'unit_mrp']
                        
#                             responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().addtocolass(
#                                 classOBJ=MODELS_ORDE.Orderitems, 
#                                 Serializer=POST_SRLZER_ORDE.Orderitemsserializer, 
#                                 data=prepare_data, 
#                                 # extra_fields=extra_fields,
#                                 required_fields=required_fields,
#                             )
#                             response_message = responsemessage
#                             response_successflag = responsesuccessflag
#                             response_data = responsedata.data
#                             response_status = responsestatus
#     return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)


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
