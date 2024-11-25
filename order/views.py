from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from helps.decorators.decorator import CommonDecorator as deco
from zone import models as MODELS_ZONE
from order import models as MODELS_ORDE
from order import models as MODELS_ORDE
from user import models as MODELS_USER
from product import models as MODELS_PROD
from account import models as MODELS_ACCO
from otp import sendotp 
from account.serializer.GET import serializers as GET_SRLZER_ACCO
from account.serializer.POST import serializers as POST_SRLZER_ACCO
from order.serializer.GET import serializers as GET_SRLZER_ORDE
from order.serializer.POST import serializers as POST_SRLZER_ORDE
from order.serializer.CUSTOM import serializers as CUST_SRLZER_ORDE
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
from otp import models as MODELS_OTP

# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@deco.get_permission(['view_order'])
def getordersummary(request):
    filter_fields = [
        {'name': 'id', 'convert': None, 'replace':'id'},
        {'name': 'customer', 'convert': None, 'replace':'user'},
        {'name': 'customer_name', 'convert': None, 'replace':'user__name__icontains'},  ##nested search
        {'name': 'customer_contact_no', 'convert': None, 'replace':'user__contact_no__icontains'}, ##nested search
        {'name': 'customer_email', 'convert': None, 'replace':'user__email__icontains'}, ##nested search
        # {'name': 'order', 'convert': None, 'replace':'orderitems_ordersummary__ordersummary'}, ##reverse nested search
        
        #date range
        {'name': 'date_from', 'convert': None, 'replace':'date__gte'},
        {'name': 'date_to', 'convert': None, 'replace':'date__lte'},

        # {'name': 'deliveryzone', 'convert': None, 'replace':'deliveryzone__name__icontains'},

        {'name': 'invoice_no', 'convert': None, 'replace':'invoice_no__icontains'},
        {'name': 'deliveryzone', 'convert': None, 'replace':'deliveryzone'},
        {'name': 'payment_mode', 'convert': None, 'replace':'payment_mode'},
        {'name': 'product_cost', 'convert': None, 'replace':'product_cost'},
        {'name': 'delivery_cost', 'convert': None, 'replace':'delivery_cost'},
        {'name': 'coupon', 'convert': None, 'replace':'coupon'},
        {'name': 'discount', 'convert': None, 'replace':'discount'},
        {'name': 'free_delivery', 'convert': 'bool', 'replace':'free_delivery'},
        {'name': 'grand_total', 'convert': None, 'replace':'grand_total'},
        {'name': 'total_profit', 'convert': None, 'replace':'total_profit'},
        {'name': 'order_status', 'convert': None, 'replace':'order_status__icontains'},
        {'name': 'payment_status', 'convert': None, 'replace':'payment_status__icontains'},
        {'name': 'order_note', 'convert': None, 'replace':'order_note__icontains'},
    ]
    ordersummarys = MODELS_ORDE.Ordersummary.objects.filter(**ghelp().KWARGS(request, filter_fields))

    ordersummarys, total_count, page, page_size = ghelp().getPaginatedData(request, ordersummarys)

    ordersummaryserializers = CUST_SRLZER_ORDE.Ordersummaryserializer(ordersummarys, many=True)
    return Response({'data': {
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'results': ordersummaryserializers.data
    }, 'message': [], 'status': 'success'}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@deco.get_permission(['view_order_item'])
def getorderitems(request):
    filter_fields = [
        {'name': 'id', 'convert': None, 'replace':'id'},
        {'name': 'ordersummary', 'convert': None, 'replace':'ordersummary'},
        {'name': 'invoice_no', 'convert': None, 'replace':'ordersummary__invoice_no__icontains'}, #came from order summary
        {'name': 'product', 'convert': None, 'replace':'product'},
        {'name': 'order_quantity', 'convert': None, 'replace':'order_quantity'},
        {'name': 'unit_trade_price', 'convert': None, 'replace':'unit_trade_price'},
        {'name': 'unit_mrp', 'convert': None, 'replace':'unit_mrp'},
    ]
    orderitems = MODELS_ORDE.Orderitems.objects.filter(**ghelp().KWARGS(request, filter_fields))

    orderitems, total_count, page, page_size = ghelp().getPaginatedData(request, orderitems)

    orderitemsserializers = GET_SRLZER_ORDE.Orderitemsserializer(orderitems, many=True)
    return Response({'data': {
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'results': orderitemsserializers.data
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
def addorder_noauth(request):
    response_data = {}
    response_message = []
    otp_message = {}
    response_successflag = 'error'
    response_status = status.HTTP_400_BAD_REQUEST
    requestdata = request.data.copy()

    last_order_id = MODELS_ORDE.Storeorderid.objects.all().order_by('id').last()
    if not last_order_id : 
        prepare_data={'last_order_id': 1}
        ghelp().addtocolass(classOBJ=MODELS_ORDE.Storeorderid, Serializer=POST_SRLZER_ORDE.Storeorderidserializer,data=prepare_data)

    contact_no = request.data.get('contact_no')
    contact_no = '8801' + contact_no[-9:]
    otp = request.data.get('otp')
    if contact_no and otp:
        otp_message = sendotp.verify_otp(contact_no , otp)

        if otp_message['flag']:
        # if True:
            userid = request.user.id
            free_delivery = True
            # if contact_no:
            delevaryzoneid = requestdata.get('deliveryzone')
            deliverycost = 0
            if delevaryzoneid:
                delevaryzone = MODELS_ZONE.Deliveryzone.objects.filter(id=delevaryzoneid)
                if delevaryzone.exists():
                    if not requestdata.get('free_delivery'):
                        deliverycost = delevaryzone.first().cost if delevaryzone.first().cost else 0
                        free_delivery = False
                    
                    todate = date.today()
                    order_note = requestdata.get('order_note')
                    payment_mode = requestdata.get('payment_mode') ## frontend theke valu dile recive korbe na dile none pathabe
                    if not payment_mode:
                        payment_mode = CHOICE.PAYMENT_MODE[0][0]
                    
                    product_costs = requestdata.get('product_cost')
                    try: product_costs += 0
                    except: response_message.append('product_costs should be type of float!')
                    grand_totals = requestdata.get('grand_total')
                    try: grand_totals += 0
                    except: response_message.append('grand_totals should be type of float!')
                    discounts = requestdata.get('discount')
                    try: discounts += 0
                    except: discounts = 0
                        # response_message.append('discounts should be type of float!')

                    ##create customer
                    if not response_message:
                        response = ghelp().purifyProducts(MODELS_PROD.Product, requestdata)
                        if not response['message']:
                            user = MODELS_USER.User.objects.filter(contact_no=contact_no)
                            print(user)
                            print( not user.exists())
                            if not user.exists():
                                contact_no = '8801' + contact_no[-9:]
                                allowed_fields = ['name', 'address', 'contact_no', 'email']
                                extra_fields = {'username': contact_no, 'password': make_password(f'PASS{contact_no}'), 'user_type': CHOICE.USER_TYPE[1][1], 'created_by': userid, 'updated_by': userid}
                                required_fields = ['name', 'address', 'contact_no']
                                fields_regex = [{'field': 'contact_no', 'type': 'phonenumber'}]
                                unique_fields=['contact_no']
                                responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().addtocolass(
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
                            if user.exists(): 
                                user = user.first()
                                userid = user.id
                                # userid = request.user.id
                                contact_no = '8801' + contact_no[-9:]
                                request.data['contact_no'] = contact_no
                                extra_fields = {}
                                if userid: extra_fields.update({'updated_by': userid})
                                allowed_fields=['name', 'address', 'contact_no', 'email']
                                # freez_update = [{'user_type': 'Admin'}]  //user type admin paile purai r update korte dibe na
                                responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().updaterecord(
                                    classOBJ=MODELS_USER.User, 
                                    Serializer=POST_SRLZER_USER.Userserializer, 
                                    id=user.id,
                                    data=request.data,
                                    allowed_fields = allowed_fields,
                                    unique_fields=['contact_no'],
                                    # freez_update=freez_update,
                                    extra_fields=extra_fields
                                )
                                if responsesuccessflag == 'success': user = responsedata.instance
                                elif responsesuccessflag == 'error': response_message.extend(responsemessage)
                            
                            if not response_message:
                                discount = 0
                                product_cost, grand_total, total_profit = ghelp().calculateProductCalculation(response['products'], discount, deliverycost)
                                if product_cost != product_costs: response_message.append(f'total calculated product_cost is not matching, calculated({product_cost}) != provided({product_costs})')
                                if grand_total != grand_totals: response_message.append(f'calculated grand_total is not matching, calculated({grand_total}) != provided({grand_totals})')
                                if discount != discounts: response_message.append(f'calculated discount is not matching, calculated({discount}) != provided({discounts})')
                                

                                ##create ordersummary
                                if not response_message:
                                    #invoice auto create
                                    last_order_id = MODELS_ORDE.Storeorderid.objects.all().order_by('id').last()
                                    inv_first_serial = 100000
                                    inv_current_serial = inv_first_serial + last_order_id.last_order_id + 1 if last_order_id else inv_first_serial + 1
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
                                        'payment_mode': payment_mode,
                                        'order_note': order_note if order_note else ""
                                    } 
                                    required_fields = ['deliveryzone']
                                    responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().addtocolass(
                                        classOBJ=MODELS_ORDE.Ordersummary,
                                        Serializer=POST_SRLZER_ORDE.Ordersummaryserializer,
                                        data=prepare_data,
                                        required_fields=required_fields
                                    )

                                    #store last order id
                                    if responsesuccessflag == 'success':
                                        last_order_id = MODELS_ORDE.Storeorderid.objects.all().order_by('id').last()
                                        if last_order_id : 
                                            prepare_data={'last_order_id': responsedata.data['id']}
                                            ghelp().updaterecord(classOBJ=MODELS_ORDE.Storeorderid, Serializer=POST_SRLZER_ORDE.Storeorderidserializer, id=last_order_id.id,data=prepare_data)
            
                                    
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
            # else: response_message.append('please provide contact number!')
            if response_successflag == 'success':
                otp_instance = MODELS_OTP.Otp.objects.filter(phone=contact_no, otp_code=otp)
                if otp_instance.exists():
                    otp_instance.delete()
        else:
            if 'OTP has expired.' in otp_message['message']:
                otp_instance = MODELS_OTP.Otp.objects.filter(phone=contact_no, otp_code=otp)
                if otp_instance.exists():
                    otp_instance.delete()
    else: response_message.append('please provide contact number and OTP!')
    return Response({'data': response_data, 'otp': otp_message, 'message': response_message, 'status': response_successflag}, status=response_status)




@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@deco.get_permission(['edit_order_status'])
def updateorderstatus(request, ordersummaryid=None):
    response_data = {}
    response_message = []
    response_successflag = 'error'
    response_status = status.HTTP_400_BAD_REQUEST

    requestdata = request.data.copy()
    userid = request.user.id
    new_order_status = requestdata.get('order_status')
    new_payment_status = requestdata.get('payment_status')
    # print("new_payment_statusnew_payment_status",new_payment_status)
    
    if ordersummaryid:
        ordersummary = MODELS_ORDE.Ordersummary.objects.filter(id=ordersummaryid)
        if ordersummary.exists():
            previous_order_status = ordersummary.first().order_status
            # print('previous_order_statusprevious_order_status', previous_order_status)
            previous_payment_status = ordersummary.first().payment_status
            print('previous_order_statusprevious_order_status', previous_payment_status)
            if new_order_status:
                
                if previous_order_status == CHOICE.ORDER_STATUS[3][1]: #Deliver
                    if new_order_status == CHOICE.ORDER_STATUS[5][1]: # REturn
                        #update product quantity
                        orderitems = MODELS_ORDE.Orderitems.objects.filter(ordersummary=ordersummaryid)
                        for orderitem in orderitems:
                            product = orderitem.product
                            productid = product.id
                            order_quantity = orderitem.order_quantity
                            product = MODELS_PROD.Product.objects.filter(id=productid)
                            quantity = product.first().quntity
                            quantity += order_quantity
                            prepare_data={'quntity': quantity}
                            response_data, response_message, response_successflag, response_status = ghelp().updaterecord(classOBJ=MODELS_PROD.Product, Serializer=POST_SRLZER_PROD.Productserializer, id=productid,data=prepare_data)
                            response_data = response_data.data if response_successflag == 'success' else {}

                        #updatr order status 
                        if response_successflag == 'success':
                            prepare_data={'order_status': new_order_status}
                            response_data, response_message, response_successflag, response_status = ghelp().updaterecord(classOBJ=MODELS_ORDE.Ordersummary, Serializer=POST_SRLZER_ORDE.Ordersummaryserializer, id=ordersummaryid,data=prepare_data)
                            response_data = response_data.data if response_successflag == 'success' else {}
                    else: response_message.append(f"{previous_order_status} product can/'t updated to {new_order_status}")
                
                elif previous_order_status in [CHOICE.ORDER_STATUS[0][1], CHOICE.ORDER_STATUS[1][1], CHOICE.ORDER_STATUS[2][1]]: #Pending, On Process, Hand to curiar
                    if new_order_status != CHOICE.ORDER_STATUS[5][1]: #not return
                        #update product quantity
                        if new_order_status == CHOICE.ORDER_STATUS[4][1]: #cancel
                            orderitems = MODELS_ORDE.Orderitems.objects.filter(ordersummary=ordersummaryid)
                            for orderitem in orderitems:
                                product = orderitem.product
                                productid = product.id
                                order_quantity = orderitem.order_quantity
                                product = MODELS_PROD.Product.objects.filter(id=productid)
                                quantity = product.first().quntity
                                quantity += order_quantity
                                prepare_data={'quntity': quantity}
                                response_data, response_message, response_successflag, response_status = ghelp().updaterecord(classOBJ=MODELS_PROD.Product, Serializer=POST_SRLZER_PROD.Productserializer, id=productid,data=prepare_data)
                                response_data = response_data.data if response_successflag == 'success' else {}
                        #updatr order status 

                        prepare_data={'order_status': new_order_status}
                        response_data, response_message, response_successflag, response_status = ghelp().updaterecord(classOBJ=MODELS_ORDE.Ordersummary, Serializer=POST_SRLZER_ORDE.Ordersummaryserializer, id=ordersummaryid,data=prepare_data)
                        response_data = response_data.data if response_successflag == 'success' else {}
                    # if new_order_status != CHOICE.ORDER_STATUS[3][1]: #Deliver
                    else: response_message.append(f"{previous_order_status} product can/'t updated to {new_order_status}")
                elif previous_order_status in [CHOICE.ORDER_STATUS[4][1], CHOICE.ORDER_STATUS[5][1]]: response_message.append(f"Status is already {new_order_status}")
            
#### payment_status
        
            if new_payment_status:
                income = MODELS_ACCO.Income.objects.filter(title='Sales')
                incomeid = income.first().id if income.exists() else None
                # create an income named in 'Sales' if sales is not exist
                if incomeid == None:
                    extra_fields = {}
                    prepare_data={'title': 'Sales', 'balance': 0}
                    if userid: extra_fields.update({'created_by': request.user.id, 'updated_by': request.user.id})
                    required_fields = ['title', 'balance']
                    response_data, response_message, responsesuccessflag, response_status = ghelp().addtocolass(
                    classOBJ=MODELS_ACCO.Income, 
                    Serializer=POST_SRLZER_ACCO.Incomeserializer, 
                    data=prepare_data, 
                    unique_fields=[], 
                    extra_fields=extra_fields, 
                    required_fields=required_fields
                    )
                    incomeid = response_data.instance.id
                    income = MODELS_ACCO.Income.objects.filter(id=incomeid)

                grand_total = ordersummary.first().grand_total

                if previous_payment_status == CHOICE.PAYMENT_STATUS[2][1]: #previous recive
                        if new_payment_status in [CHOICE.PAYMENT_STATUS[1][1], CHOICE.PAYMENT_STATUS[0][1]]: #new partial, pending
                            response_message.append(f"({previous_payment_status}) product can/'t updated to ({new_payment_status})")
                
                elif previous_payment_status == CHOICE.PAYMENT_STATUS[1][1]: #previous partial
                    if new_payment_status == CHOICE.PAYMENT_STATUS[2][1]: #new recive
                        transections = MODELS_ACCO.Transection.objects.filter(ordersummary=ordersummaryid)
                        if incomeid:
                            if transections:
                                sum_partial_amount = 0
                                for transection in transections:
                                    partial_amount = transection.amount
                                    sum_partial_amount += partial_amount

                                if sum_partial_amount < grand_total:
                                    rest_amount = grand_total - sum_partial_amount
                                
                                income_balance = income.first().balance
                                income_balance = income_balance + rest_amount
                                #updatte income
                                extra_fields = {}
                                if userid: extra_fields.update({'updated_by': userid})
                                prepare_data={'balance': income_balance}
                                responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().updaterecord(
                                    classOBJ=MODELS_ACCO.Income, 
                                    Serializer=POST_SRLZER_ACCO.Incomeserializer, 
                                    id=incomeid,
                                    data=prepare_data,
                                    extra_fields=extra_fields
                                )
                                response_data = responsedata.data if responsesuccessflag == 'success' else {}
                                #create transiction
                                if responsesuccessflag == 'success':
                                    todate = date.today()
                                    required_fields = ['date', 'amount']
                                    # fields_regex = [{'field': 'date', 'type': 'date'}]
                                    prepare_data={'income': incomeid, 'ordersummary': ordersummaryid, 'date': todate, 'amount': rest_amount}
                                    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(
                                        classOBJ=MODELS_ACCO.Transection, 
                                        Serializer=POST_SRLZER_ACCO.Transectionserializer, 
                                        data=prepare_data, 
                                        # unique_fields=[], 
                                        # fields_regex=fields_regex, 
                                        required_fields=required_fields,
                                    )
                                    if response_data: response_data = response_data.data
                                    #update order payment status
                                    if response_successflag=='success':
                                        prepare_data={'payment_status': new_payment_status}
                                        response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
                                            classOBJ=MODELS_ORDE.Ordersummary, 
                                            Serializer=POST_SRLZER_ORDE.Ordersummaryserializer, 
                                            id=ordersummaryid,
                                            data=prepare_data
                                        )
                                        response_data = response_data.data if response_successflag == 'success' else {}

                    elif new_payment_status == CHOICE.PAYMENT_STATUS[1][1]: #new partial
                        transections = MODELS_ACCO.Transection.objects.filter(ordersummary=ordersummaryid)
                        if incomeid:
                            if transections:
                                sum_partial_amount = 0
                                for transection in transections:
                                    partial_amount = transection.amount
                                    sum_partial_amount += partial_amount

                                if sum_partial_amount < grand_total:
                                    rest_amount = grand_total - sum_partial_amount
                                new_partial_amount = requestdata.get('partial_amount')
                                if new_partial_amount:
                                    if new_partial_amount > rest_amount:
                                        response_message.append(f"{new_partial_amount} is is greater than due money {rest_amount}")
                                    elif new_partial_amount == rest_amount:
                                        #update income
                                        income_balance = income.first().balance
                                        income_balance = income_balance + new_partial_amount
                                        extra_fields = {}
                                        if userid: extra_fields.update({'updated_by': userid})
                                        prepare_data={'balance': income_balance}
                                        responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().updaterecord(
                                            classOBJ=MODELS_ACCO.Income, 
                                            Serializer=POST_SRLZER_ACCO.Incomeserializer, 
                                            id=incomeid,
                                            data=prepare_data,
                                            extra_fields=extra_fields
                                        )
                                        response_data = responsedata.data if responsesuccessflag == 'success' else {}
                                        #create transiction
                                        if responsesuccessflag == 'success':
                                            todate = date.today()
                                            required_fields = ['date', 'amount']
                                            # fields_regex = [{'field': 'date', 'type': 'date'}]
                                            prepare_data={'income': incomeid, 'ordersummary': ordersummaryid, 'date': todate, 'amount': new_partial_amount}
                                            response_data, response_message, response_successflag, response_status = ghelp().addtocolass(
                                                classOBJ=MODELS_ACCO.Transection, 
                                                Serializer=POST_SRLZER_ACCO.Transectionserializer, 
                                                data=prepare_data, 
                                                # fields_regex=fields_regex, 
                                                required_fields=required_fields,
                                            )
                                            if response_data: response_data = response_data.data

                                        #update payment status reacive
                                        if response_successflag=='success':
                                            prepare_data={'payment_status': CHOICE.PAYMENT_STATUS[2][1]}
                                            response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
                                                classOBJ=MODELS_ORDE.Ordersummary, 
                                                Serializer=POST_SRLZER_ORDE.Ordersummaryserializer, 
                                                id=ordersummaryid,
                                                data=prepare_data
                                            )
                                            response_data = response_data.data if response_successflag == 'success' else {}

                                    elif new_partial_amount < rest_amount:
                                        #update income
                                        income_balance = income.first().balance
                                        income_balance = income_balance + new_partial_amount
                                        extra_fields = {}
                                        if userid: extra_fields.update({'updated_by': userid})
                                        prepare_data={'balance': income_balance}
                                        responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().updaterecord(
                                            classOBJ=MODELS_ACCO.Income, 
                                            Serializer=POST_SRLZER_ACCO.Incomeserializer, 
                                            id=incomeid,
                                            data=prepare_data,
                                            extra_fields=extra_fields
                                        )
                                        response_data = responsedata.data if responsesuccessflag == 'success' else {}
                                        #create transiction
                                        if responsesuccessflag == 'success':
                                            todate = date.today()
                                            required_fields = ['date', 'amount']
                                            # fields_regex = [{'field': 'date', 'type': 'date'}]
                                            prepare_data={'income': incomeid, 'ordersummary': ordersummaryid, 'date': todate, 'amount': new_partial_amount}
                                            response_data, response_message, response_successflag, response_status = ghelp().addtocolass(
                                                classOBJ=MODELS_ACCO.Transection, 
                                                Serializer=POST_SRLZER_ACCO.Transectionserializer, 
                                                data=prepare_data, 
                                                # fields_regex=fields_regex, 
                                                required_fields=required_fields,
                                            )
                                            if response_data: response_data = response_data.data

                                        #update payment status reacive
                                        if response_successflag=='success':
                                            prepare_data={'payment_status': new_payment_status}
                                            response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
                                                classOBJ=MODELS_ORDE.Ordersummary, 
                                                Serializer=POST_SRLZER_ORDE.Ordersummaryserializer, 
                                                id=ordersummaryid,
                                                data=prepare_data
                                            )
                                            response_data = response_data.data if response_successflag == 'success' else {}
                                    
                    else: response_message.append(f"{previous_payment_status} product can/'t updated to {new_payment_status}")
                elif previous_payment_status == CHOICE.PAYMENT_STATUS[0][1]: #previous pending
                    if new_payment_status in [CHOICE.PAYMENT_STATUS[1][1], CHOICE.PAYMENT_STATUS[2][1]]: #new partial / recive
                        #update income
                        if incomeid:
                            amount = 0
                            if new_payment_status == CHOICE.PAYMENT_STATUS[1][1]: #new partial
                                partial_amount = requestdata.get('partial_amount')
                                if partial_amount:
                                    if partial_amount < grand_total:
                                        amount = partial_amount
                                    elif partial_amount == grand_total:
                                        amount = grand_total
                                        new_payment_status = CHOICE.PAYMENT_STATUS[2][1]

                                    else: response_message.append(f"({partial_amount}) is greater than ({grand_total})")
                            else: 
                                amount = grand_total
                                new_payment_status = CHOICE.PAYMENT_STATUS[2][1]
                            income_balance = income.first().balance
                            if amount:
                                income_balance = income_balance + amount
                            else :
                                partial_amount = 0
                                income_balance = income_balance + amount
                            if not response_message:
                                extra_fields = {}
                                if userid: extra_fields.update({'updated_by': userid})
                                prepare_data={'balance': income_balance}
                                responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().updaterecord(
                                    classOBJ=MODELS_ACCO.Income, 
                                    Serializer=POST_SRLZER_ACCO.Incomeserializer, 
                                    id=incomeid,
                                    data=prepare_data,
                                    extra_fields=extra_fields
                                )
                                response_data = responsedata.data if responsesuccessflag == 'success' else {}
                                #create transiction
                                if responsesuccessflag == 'success':
                                    todate = date.today()
                                    required_fields = ['date', 'amount']
                                    # fields_regex = [{'field': 'date', 'type': 'date'}]
                                    prepare_data={'income': incomeid, 'ordersummary': ordersummaryid, 'date': todate, 'amount': amount}
                                    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(
                                        classOBJ=MODELS_ACCO.Transection, 
                                        Serializer=POST_SRLZER_ACCO.Transectionserializer, 
                                        data=prepare_data, 
                                        # fields_regex=fields_regex, 
                                        required_fields=required_fields,
                                    )
                                    if response_data: response_data = response_data.data
                                    #update order payment status
                                    if response_successflag=='success':
                                        prepare_data={'payment_status': new_payment_status}
                                        response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
                                            classOBJ=MODELS_ORDE.Ordersummary, 
                                            Serializer=POST_SRLZER_ORDE.Ordersummaryserializer, 
                                            id=ordersummaryid,
                                            data=prepare_data
                                        )
                                        response_data = response_data.data if response_successflag == 'success' else {}
        else: response_message.append("order summary dose/'t exist!")
    else: response_message.append('order_status is required!')
    if response_message:
        response_successflag = 'error'
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)





@api_view(['POST'])
@permission_classes([IsAuthenticated])
@deco.get_permission(['create_order'])
def addorder_auth(request):
    response_data = {}
    response_message = []
    response_successflag = 'error'
    response_status = status.HTTP_400_BAD_REQUEST
    requestdata = request.data.copy()

    last_order_id = MODELS_ORDE.Storeorderid.objects.all().order_by('id').last()
    if not last_order_id : 
        prepare_data={'last_order_id': 1}
        ghelp().addtocolass(classOBJ=MODELS_ORDE.Storeorderid, Serializer=POST_SRLZER_ORDE.Storeorderidserializer,data=prepare_data)


    userid = request.user.id
    free_delivery = True
    customerid = request.data.get('customer')
    if customerid:
        delevaryzoneid = requestdata.get('deliveryzone')
        deliverycost = 0
        if delevaryzoneid:
            delevaryzone = MODELS_ZONE.Deliveryzone.objects.filter(id=delevaryzoneid)
            if delevaryzone.exists():
                if not requestdata.get('free_delivery'):
                    deliverycost = delevaryzone.first().cost if delevaryzone.first().cost else 0
                    free_delivery = False
                
                todate = date.today()
                order_note = requestdata.get('order_note')
                payment_mode = requestdata.get('payment_mode') ## frontend theke valu dile recive korbe na dile none pathabe
                if not payment_mode:
                    payment_mode = CHOICE.PAYMENT_MODE[0][0]
                
                product_costs = requestdata.get('product_cost')
                try: product_costs += 0
                except: response_message.append('product_costs should be type of float!')
                grand_totals = requestdata.get('grand_total')
                try: grand_totals += 0
                except: response_message.append('grand_totals should be type of float!')
                discount_totals = requestdata.get('discount_total')
                try: discount_totals += 0
                except: response_message.append('discount_totals should be type of float!')
                    # response_message.append('discounts should be type of float!')
                discounts = requestdata.get('discount')
                if discounts == None:
                    discounts = 0
                
                is_fiexd_amounts = requestdata.get('is_fiexd_amount')

                ##create customer
                if not response_message:
                    response = ghelp().purifyProducts(MODELS_PROD.Product, requestdata)
                    if not response['message']:
                        user = MODELS_USER.User.objects.filter(id=customerid) 
                        if user.exists():
                            product_cost, grand_total, total_profit, discount_total = ghelp().calculateProductCalculationauth(response['products'], discounts, is_fiexd_amounts, deliverycost)
                            if product_cost != product_costs: response_message.append(f'total calculated product_cost is not matching, calculated({product_cost}) != provided({product_costs})')
                            if grand_total != grand_totals: response_message.append(f'calculated grand_total is not matching, calculated({grand_total}) != provided({grand_totals})')
                            if discount_total != discount_totals: response_message.append(f'calculated discount is not matching, calculated({discount_total}) != provided({discount_totals})')
                            
                            ##create ordersummary
                            if not response_message:
                                #invoice auto create
                                last_order_id = MODELS_ORDE.Storeorderid.objects.all().order_by('id').last()
                                inv_first_serial = 100000
                                inv_current_serial = inv_first_serial + last_order_id.last_order_id + 1 if last_order_id else inv_first_serial + 1
                                invoice_no = f'INV{inv_current_serial}'

                                prepare_data={
                                    'user': customerid,
                                    'date': todate,
                                    'invoice_no': invoice_no,
                                    'deliveryzone': delevaryzoneid,
                                    'product_cost': product_cost,
                                    'delivery_cost': deliverycost,
                                    'free_delivery': free_delivery,
                                    'grand_total': grand_total,
                                    'total_profit': total_profit,
                                    'discount': discount_total,
                                    'payment_mode': payment_mode,
                                    'order_note': order_note if order_note else ""
                                } 
                                extra_fields = {}
                                if userid: extra_fields.update({'created_by': request.user.id, 'updated_by': request.user.id})
                                required_fields = ['deliveryzone']
                                responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().addtocolass(
                                    classOBJ=MODELS_ORDE.Ordersummary,
                                    Serializer=POST_SRLZER_ORDE.Ordersummaryserializer,
                                    data=prepare_data,
                                    extra_fields=extra_fields,
                                    required_fields=required_fields
                                )
                                #store last order id
                                if responsesuccessflag == 'success':
                                    last_order_id = MODELS_ORDE.Storeorderid.objects.all().order_by('id').last()
                                    if last_order_id : 
                                        prepare_data={'last_order_id': responsedata.data['id']}
                                        ghelp().updaterecord(classOBJ=MODELS_ORDE.Storeorderid, Serializer=POST_SRLZER_ORDE.Storeorderidserializer, id=last_order_id.id,data=prepare_data)
          
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
                        else: 
                            response_message.append('user id is not invalid!')      
                    else: response_message.extend(response['message'])
            else: response_message.append('delivary zone id is invalid!')
        else: response_message.append('delivary zone is required!')
    else: response_message.append('please provide valid customer')
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@deco.get_permission(['edit_order'])
def updateorder_auth(request, ordersummaryid=None):
    response_data = {}
    response_message = []
    response_successflag = 'error'
    response_status = status.HTTP_400_BAD_REQUEST

    requestdata = request.data.copy()
    previous_orderitems = MODELS_ORDE.Orderitems.objects.filter(ordersummary_id=ordersummaryid)
    new_orderitems = request.data.get('products')
    
    previous_products = []
    new_products = []
    # remove_products = []
    # remove_orderitems = []
    # update_products = []
    # update_orderitems = []
    # add_products = []

    for product in previous_orderitems:
        previous_products.append(product.product.id)
    for product in new_orderitems:
        new_products.append(product.get('id'))

    customerid = requestdata.get('customer')
    if customerid == None:
        response_message.append('customer is required!')
    free_delivery = True

    delevaryzoneid = requestdata.get('deliveryzone')
    deliverycost = 0
    if delevaryzoneid:
        delevaryzone = MODELS_ZONE.Deliveryzone.objects.filter(id=delevaryzoneid)
        if delevaryzone.exists():
            if not requestdata.get('free_delivery'):
                deliverycost = delevaryzone.first().cost if delevaryzone.first().cost else 0
                free_delivery = False
            
            todate = date.today()
            coupons = requestdata.get('coupon')
            try: coupons += 0
            except: coupons = 0
            payment_mode = requestdata.get('payment_mode') ## frontend theke valu dile recive korbe na dile none pathabe
            if not payment_mode:
                payment_mode = CHOICE.PAYMENT_MODE[0][0]
            
            product_costs = requestdata.get('product_cost')
            try: product_costs += 0
            except: response_message.append('product_costs should be type of float!')
            grand_totals = requestdata.get('grand_total')
            try: grand_totals += 0
            except: response_message.append('grand_totals should be type of float!')
            discount_totals = requestdata.get('discount_total')
            try: discount_totals += 0
            except: response_message.append('discount_totals should be type of float!')
                # response_message.append('discounts should be type of float!')

            order = MODELS_ORDE.Ordersummary.objects.get(id=ordersummaryid)
            discounts = requestdata.get('discount')
            if discounts == None:
                discounts = order.discount

            order_note = requestdata.get('order_note')
            if order_note == None:
                order_note = order.order_note
            
            is_fiexd_amounts = requestdata.get('is_fiexd_amount')
            
            ##create customer
            if not response_message:
                
                response = ghelp().purifyProducts(MODELS_PROD.Product, requestdata)
                if not response['message']:
                    user = MODELS_USER.User.objects.filter(id=customerid) 
                    if user.exists():
                        
                        product_cost, grand_total, total_profit, discount_total = ghelp().calculateProductCalculationauth(response['products'], discounts, is_fiexd_amounts, deliverycost)
                        if product_cost != product_costs: response_message.append(f'total calculated product_cost is not matching, calculated({product_cost}) != provided({product_costs})')
                        if grand_total != grand_totals: response_message.append(f'calculated grand_total is not matching, calculated({grand_total}) != provided({grand_totals})')
                        if discount_total != discount_totals: response_message.append(f'calculated discount is not matching, calculated({discount_total}) != provided({discount_totals})')

                        # print("product_cost", product_cost)
                        # print("grand_total", grand_total)
                        # print("discount_total", discount_total)

                        #update order iteam or delete order iteam and update product quantity
                        if not response_message:
                            for productid in previous_products:
                                previous_orderitem = previous_orderitems.filter(product_id=productid).first()

                                #update order iteam or delete order iteam and update product quantity
                                if productid in new_products:
                                    for product in new_orderitems:
                                        if product.get('id')==productid:
                                            new_quantity = product.get('order_quantity')

                                    previous_quantity = previous_orderitem.order_quantity
                                    quantity = new_quantity - previous_quantity

                                    # update_orderitems.append(previous_orderitem.id)
                                    # update_products.append(productid)

                                    product = MODELS_PROD.Product.objects.filter(id=productid).first()
                                    order_item = previous_orderitem.id
                                    prepare_data={
                                                'product': productid,
                                                'order_quantity': new_quantity,
                                                'unit_trade_price': product.costprice,
                                                'unit_mrp': product.mrpprice
                                            }
                                    allowed_fields=['product', 'order_quantity', 'unit_trade_price', 'unit_mrp']
                                    response_data, response_message, responsesuccessflag, response_status = ghelp().updaterecord(
                                        classOBJ=MODELS_ORDE.Orderitems, 
                                        Serializer=POST_SRLZER_ORDE.Orderitemsserializer, 
                                        id=previous_orderitem.id,
                                        data=prepare_data,
                                    )
                                    response_data = response_data.data if response_successflag == 'success' else {}
                                    if responsesuccessflag == 'success':
                                        # order_quantity = quantity
                                        product = MODELS_PROD.Product.objects.filter(id=productid)
                                        product_quantity = product.first().quntity
                                        product_quantity -= quantity
                                        prepare_data={'quntity': product_quantity}
                                        ghelp().updaterecord(classOBJ=MODELS_PROD.Product, Serializer=POST_SRLZER_PROD.Productserializer, id=productid,data=prepare_data)

                                #delete order iteam and update product quantity
                                else:
                                    # remove_orderitems.append(previous_orderitem.id)
                                    removeid = previous_orderitem.id
                                    # remove_products.append(productid)
                                    orderitem = previous_orderitems.filter(id=removeid).first()
                                    order_quantity = orderitem.order_quantity
                                    responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().deleterecord(
                                    classOBJ=MODELS_ORDE.Orderitems,
                                    id=removeid,
                                    )
                                    if responsesuccessflag == 'success':               
                                        product = MODELS_PROD.Product.objects.filter(id=productid).first()
                                        quantity = product.quntity
                                        quantity += order_quantity
                                        prepare_data={'quntity': quantity}
                                        responsedata, responsemessage, responsesuccessflag, responsestatus =ghelp().updaterecord(classOBJ=MODELS_PROD.Product, Serializer=POST_SRLZER_PROD.Productserializer, id=productid, data=prepare_data)
                            # print("previous_products", previous_products)
                            # print("new_products", new_products)

                            #add order iteam and update product quantity
                            for productid in new_products:
                                if productid not in previous_products:
                                    # add_products.append(productid)
                                    for product in new_orderitems:
                                        if product.get('id')==productid:
                                            quantity = product.get('order_quantity')
                                            
                                    product = MODELS_PROD.Product.objects.filter(id=productid)
                                    prepare_data={
                                        'ordersummary': ordersummaryid,
                                        'product': productid,
                                        'order_quantity': quantity,
                                        'unit_trade_price': product.first().costprice,
                                        'unit_mrp': product.first().mrpprice
                                    }
                                    #create orderitems
                                    responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().addtocolass(classOBJ=MODELS_ORDE.Orderitems, Serializer=POST_SRLZER_ORDE.Orderitemsserializer, data=prepare_data)
                                    response_successflag = responsesuccessflag
                                    response_data = responsedata.data
                                    response_status = responsestatus
                                    #Update product quantity
                                    if responsesuccessflag == 'success':
                                        order_quantity = quantity
                                        product = MODELS_PROD.Product.objects.filter(id=productid)
                                        quantity = product.first().quntity
                                        quantity -= order_quantity
                                        prepare_data={'quntity': quantity}
                                        ghelp().updaterecord(classOBJ=MODELS_PROD.Product, Serializer=POST_SRLZER_PROD.Productserializer, id=productid,data=prepare_data)    

                            ##update ordersummary        
                            if not response_message:
                                userid = request.user.id
                                extra_fields = {}
                                if userid: extra_fields.update({'updated_by': userid})
                                prepare_data={
                                    'user': customerid,
                                    'deliveryzone': delevaryzoneid,
                                    'product_cost': product_cost,
                                    'delivery_cost': deliverycost,
                                    'free_delivery': free_delivery,
                                    'grand_total': grand_total,
                                    'total_profit': total_profit,
                                    'discount': discount_total,
                                    'payment_mode': payment_mode,
                                    'coupon' : coupons,
                                    'order_note': order_note if order_note else ""
                                }
                                allowed_fields=['user', 'deliveryzone', 'product_cost', 'delivery_cost', 'free_delivery', 'grand_total', 'total_profit', 'discount', 'payment_mode', 'coupon']
                                response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
                                    classOBJ=MODELS_ORDE.Ordersummary, 
                                    Serializer=POST_SRLZER_ORDE.Ordersummaryserializer, 
                                    id=ordersummaryid,
                                    data=prepare_data,
                                    extra_fields=extra_fields,
                                    allowed_fields= allowed_fields
                                )
                                response_data = response_data.data if response_successflag == 'success' else {}
                    else: response_message.append('user id is not invalid!')  
                else: response_message.extend(response['message'])   
        else: response_message.append('delivary zone id is invalid!')
    else: response_message.append('delivary zone is required!')
    # print("remove_products",remove_products, remove_orderitems)
    # print("update_products",update_products, update_orderitems)
    # print("add_products",add_products)
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

