from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from user import models as MODELS_USER
from user.serializer.GET import serializers as GET_SRLZER_USER
from user.serializer.POST import serializers as POST_SRLZER_USER
from user.serializer.CUSTOM import serializers as CUSTOM_SRLZER_USER
from django.contrib.auth.hashers import make_password
# from payroll.serializer.POST import serializers as PSRLZER_PAYR
from helps.common.generic import Generichelps as ghelp
from rest_framework.response import Response
from helps.choice import common as CHOICE
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q


@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getusers(request):
    filter_fields = [
        {'name': 'id', 'convert': None, 'replace':'id'},
        {'name': 'name', 'convert': None, 'replace':'name__icontains'},
        {'name': 'address', 'convert': None, 'replace':'address__icontains'},
        {'name': 'contact_no', 'convert': None, 'replace':'acontact_no'},
        {'name': 'email', 'convert': None, 'replace':'email__icontains'}
    ]
    KWARGS = ghelp().KWARGS(request, filter_fields)
    KWARGS.update({'user_type': 'Admin'})
    users = MODELS_USER.User.objects.filter(**KWARGS)

    users, total_count, page, page_size = ghelp().getPaginatedData(request, users)

    userserializers = GET_SRLZER_USER.Userserializer(users, many=True)
    return Response({'data': {
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'results': userserializers.data
    }, 'message': [], 'status': 'success'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['get company info', 'all'])
def adduser(request):
    requestdata = request.data.copy()
    # userid = request.user.id
    # extra_fields = {}
    # if userid: extra_fields.update({'created_by': request.user.id, 'updated_by': request.user.id})
    required_fields = ['name', 'address', 'contact_no', 'password', 'username']

    prepare_data={
        'name': request.data.get('name'), 
        'contact_no': request.data.get('contact_no'), 
        'address': request.data.get('address'), 
        'username': request.data.get('username'), 
        'password': request.data.get('password'),
        'user_type': CHOICE.USER_TYPE[0][1]}
    if 'password' in requestdata: requestdata['password'] = make_password(requestdata['password'])
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(
        classOBJ=MODELS_USER.User, 
        Serializer=POST_SRLZER_USER.Userserializer, 
        data=prepare_data, 
        unique_fields=[], 
        # extra_fields=extra_fields, 
        required_fields=required_fields
    )
    if response_data: response_data = response_data.data
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def updateuser(request, uuserid=None):
    userid = request.user.id
    extra_fields = {}
    if userid: extra_fields.update({'updated_by': userid})
    allowed_fields=['name', 'address', 'contact_no', 'username', 'email']
    # freez_update = [{'user_type': 'Admin'}]  //user type admin paile purai r update korte dibe na
    response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
        classOBJ=MODELS_USER.User, 
        Serializer=POST_SRLZER_USER.Userserializer, 
        id=uuserid,
        data=request.data,
        allowed_fields = allowed_fields,
        unique_fields=['contact_no'],
        # freez_update=freez_update,
        extra_fields=extra_fields
    )
    response_data = response_data.data if response_successflag == 'success' else {}
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def deleteuser(request, uuserid=None):
    response_data, response_message, response_successflag, response_status = ghelp().deleterecord(
        classOBJ=MODELS_USER.User,
        id=uuserid,
        
    )
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

















@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getcustomers(request):
    filter_fields = [
        {'name': 'id', 'convert': None, 'replace':'id'},
        {'name': 'name', 'convert': None, 'replace':'name__icontains'},
        {'name': 'address', 'convert': None, 'replace':'address__icontains'},
        {'name': 'contact_no', 'convert': None, 'replace':'contact_no'},
        {'name': 'email', 'convert': None, 'replace':'email__icontains'},
        # {'name': 'customer', 'convert': None, 'replace':'user__icontains'},
        

        # one search feild many atribute at a time.
        # {'name': 'attendance_mode', 'convert': 'list-str', 'split': '--', 'replace':'attendance_mode__in'},
        # {'name': 'attendance_status', 'convert': 'list-str', 'split': '!!', 'replace':'attendance_status__contains'}, AND
        # {'name': 'attendance_status', 'convert': 'list-str', 'split': '--', 'replace':'attendance_status__overlap'}, # OR
    ]

    KWARGS = ghelp().KWARGS(request, filter_fields)
    KWARGS.update({'user_type': 'Customer'})
    customers = MODELS_USER.User.objects.filter(**KWARGS)
    
    #One sheach feild at a time 1 atribute but options will many
    #the filter will look for the search_term in the name, contact_no, or email fields.
    search_term = request.GET.get('search_term')
    if search_term != None:
        customers = customers.filter(Q(name__icontains=search_term) | Q(email__icontains=search_term) | Q(contact_no__icontains=search_term))

    customers, total_count, page, page_size = ghelp().getPaginatedData(request, customers)
    userserializers = CUSTOM_SRLZER_USER.Userserializer(customers, many=True)
    return Response({'data': {
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'results': userserializers.data
    }, 'message': [], 'status': 'success'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['get company info', 'all'])
def addcustomer(request):
    name = request.data.get('name')
    contact_no = request.data.get('contact_no')
    email = request.data.get('email')
    address = request.data.get('address')
    password = f'PASS{contact_no}'
    username = contact_no
    requestdata = request.data.copy()
    userid = request.user.id
    extra_fields = {}

    if userid: extra_fields.update({'created_by': request.user.id, 'updated_by': request.user.id})
    prepare_data={'name': name, 'contact_no': contact_no, 'address': address, 'username': username, 'password': password}
    if email:
        prepare_data={'name': name, 'contact_no': contact_no, 'address': address, 'username': username, 'password': password, 'email': email}
    
    required_fields = ['name', 'address', 'contact_no']
    if 'password' in requestdata: requestdata['password'] = make_password(requestdata['password'])
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(
        classOBJ=MODELS_USER.User, 
        Serializer=POST_SRLZER_USER.Userserializer, 
        data=prepare_data, 
        unique_fields=['contact_no'], 
        extra_fields=extra_fields, 
        required_fields=required_fields
    )
    if response_data: response_data = response_data.data
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def updatecustomer(request, customerid=None):
    userid = request.user.id
    extra_fields = {}
    if userid: extra_fields.update({'updated_by': userid})
    allowed_fields=['name', 'address', 'contact_no', 'email']
    # freez_update = [{'user_type': 'Admin'}]  //user type admin paile purai r update korte dibe na
    response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
        classOBJ=MODELS_USER.User, 
        Serializer=POST_SRLZER_USER.Userserializer, 
        id=customerid,
        data=request.data,
        allowed_fields = allowed_fields,
        unique_fields=['contact_no'],
        # freez_update=freez_update,
        extra_fields=extra_fields
    )
    response_data = response_data.data if response_successflag == 'success' else {}
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def deletecustomer(request, customerid=None):
    response_data, response_message, response_successflag, response_status = ghelp().deleterecord(
        classOBJ=MODELS_USER.User,
        id=customerid,
        
    )
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)
