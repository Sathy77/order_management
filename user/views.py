from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from helps.decorators.decorator import CommonDecorator as deco
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
# @deco.get_permission(['view_permission'])
def getpermissioncategory(request):
    filter_fields = [
        {'name': 'id', 'convert': None, 'replace':'id'},
        {'name': 'name', 'convert': None, 'replace':'name__icontains'},
    ]
    permissioncategories = MODELS_USER.Permissioncategory.objects.filter(**ghelp().KWARGS(request, filter_fields))

    permissioncategories, total_count, page, page_size = ghelp().getPaginatedData(request, permissioncategories)

    permissioncategoryserializers = GET_SRLZER_USER.Permissioncategoryserializer(permissioncategories, many=True)
    return Response({'data': {
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'results': permissioncategoryserializers.data
    }, 'message': [], 'status': 'success'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['view_permission'])
def getpermissions(request):
    filter_fields = [
        {'name': 'id', 'convert': None, 'replace':'id'},
        {'name': 'name', 'convert': None, 'replace':'name__icontains'},
    ]
    permissions = MODELS_USER.Permission.objects.filter(**ghelp().KWARGS(request, filter_fields))

    permissions, total_count, page, page_size = ghelp().getPaginatedData(request, permissions)

    permissionsserializers = GET_SRLZER_USER.Permissionserializer(permissions, many=True)
    return Response({'data': {
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'results': permissionsserializers.data
    }, 'message': [], 'status': 'success'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['create_permission'])
def addpermission(request):
    requestdata = request.data.copy()
    # userid = request.user.id
    # extra_fields = {}
    # if userid: extra_fields.update({'created_by': request.user.id, 'updated_by': request.user.id})
    required_fields = ['name']
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(
        classOBJ=MODELS_USER.Permission, 
        Serializer=POST_SRLZER_USER.Permissionserializer, 
        data=requestdata, 
        unique_fields=[], 
        required_fields=required_fields
    )
    if response_data: response_data = response_data.data
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['edit_permission'])
def updatepermission(request, permissionid=None):
    # userid = request.user.id
    # extra_fields = {}
    # if userid: extra_fields.update({'updated_by': userid})
    response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
        classOBJ=MODELS_USER.Permission, 
        Serializer=POST_SRLZER_USER.Permissionserializer, 
        id=permissionid,
        data=request.data,
        # extra_fields=extra_fields
    )
    response_data = response_data.data if response_successflag == 'success' else {}
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['delete_permission'])
def deletepermission(request, permissionid=None):
    response_data, response_message, response_successflag, response_status = ghelp().deleterecord(
        classOBJ=MODELS_USER.Permission,
        id=permissionid,
    )
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['view_role'])
def getroles(request):
    filter_fields = [
        {'name': 'id', 'convert': None, 'replace':'id'},
        {'name': 'name', 'convert': None, 'replace':'name__icontains'},
        {'name': 'permission', 'convert': None, 'replace':'permission__icontains'},
    ]
    roles = MODELS_USER.Role.objects.filter(**ghelp().KWARGS(request, filter_fields))

    roles, total_count, page, page_size = ghelp().getPaginatedData(request, roles)

    rolesserializers = CUSTOM_SRLZER_USER.Roleserializer(roles, many=True)
    return Response({'data': {
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'results': rolesserializers.data
    }, 'message': [], 'status': 'success'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['create_role'])
def addrole(request):
    requestdata = request.data.copy()
    # userid = request.user.id
    # extra_fields = {}
    # if userid: extra_fields.update({'created_by': request.user.id, 'updated_by': request.user.id})
    required_fields = ['name', 'permission']
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(
        classOBJ=MODELS_USER.Role, 
        Serializer=POST_SRLZER_USER.Roleserializer, 
        data=requestdata, 
        unique_fields=[], 
        required_fields=required_fields
    )
    if response_data: response_data = response_data.data
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['edit_role'])
def updaterole(request, roleid=None):
    response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
        classOBJ=MODELS_USER.Role, 
        Serializer=POST_SRLZER_USER.Roleserializer, 
        id=roleid,
        data=request.data,
    )
    response_data = response_data.data if response_successflag == 'success' else {}
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['delete_role'])
def deleterole(request, roleid=None):
    response_data, response_message, response_successflag, response_status = ghelp().deleterecord(
        classOBJ=MODELS_USER.Role,
        id=roleid,
    )
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
@deco.get_permission(['view_user'])
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
@deco.get_permission(['create_user'])
def adduser(request):
    requestdata = request.data.copy()
    # userid = request.user.id
    # extra_fields = {}
    # if userid: extra_fields.update({'created_by': request.user.id, 'updated_by': request.user.id})
    if 'username' in requestdata: requestdata['username'] = requestdata['username'].lower()
    if 'password' in requestdata: requestdata['password'] = make_password(requestdata['password'])
    required_fields = ['name', 'address', 'contact_no', 'password', 'username', 'role']
    email = requestdata.get('email')
    contact_no = requestdata.get('contact_no')
    contact_no = '8801' + contact_no[-9:]
    prepare_data={
        'name': requestdata.get('name'),
        'contact_no': contact_no,
        'address': requestdata.get('address'),
        'username': requestdata.get('username'),
        'password': requestdata.get('password'),  # Hashed password
        'user_type': CHOICE.USER_TYPE[0][1],
        'role': requestdata.get('role'),
        'email': email if email else ""}
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
@deco.get_permission(['edit_user'])
def updateuser(request, uuserid=None):
    requestdata = request.data.copy()
    userid = request.user.id
    contact_no = requestdata.get('contact_no')
    contact_no = '8801' + contact_no[-9:]
    extra_fields = {}
    if userid: extra_fields.update({'updated_by': userid})
    if 'username' in requestdata: requestdata['username'] = requestdata['username'].lower()
    if 'password' in requestdata: requestdata['password'] = make_password(requestdata['password'])
    allowed_fields=['name', 'address', 'contact_no', 'username', 'email', 'role', 'password']
    # freez_update = [{'user_type': 'Admin'}]  //user type admin paile purai r update korte dibe na
    response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
        classOBJ=MODELS_USER.User, 
        Serializer=POST_SRLZER_USER.Userserializer, 
        id=uuserid,
        data=requestdata,
        allowed_fields = allowed_fields,
        unique_fields=['contact_no'],
        # freez_update=freez_update,
        extra_fields=extra_fields
    )
    response_data = response_data.data if response_successflag == 'success' else {}
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@deco.get_permission(['delete_user'])
def deleteuser(request, uuserid=None):
    response_data, response_message, response_successflag, response_status = ghelp().deleterecord(
        classOBJ=MODELS_USER.User,
        id=uuserid,
        
    )
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

















@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['view_customer'])
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
# @deco.get_permission(['create_customer'])
def addcustomer(request):
    requestdata = request.data.copy()
    name = requestdata.get('name')
    contact_no = requestdata.get('contact_no')
    contact_no = '8801' + contact_no[-9:]
    email = requestdata.get('email')
    address = requestdata.get('address')
    password = f'PASS{contact_no}'
    password = make_password(password)
    username = contact_no
    userid = request.user.id
    extra_fields = {}

    if userid: extra_fields.update({'created_by': request.user.id, 'updated_by': request.user.id})
    # if 'password' in requestdata: requestdata['password'] = make_password(password)
    prepare_data={'name': name, 'contact_no': contact_no, 'address': address, 'username': username, 'password': password, 'email': email if email else ""}
    # if email:
    #     prepare_data={'name': name, 'contact_no': contact_no, 'address': address, 'username': username, 'password': password, 'email': email}
    
    required_fields = ['name', 'address', 'contact_no']
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
# @deco.get_permission(['edit_customer'])
def updatecustomer(request, customerid=None):
    userid = request.user.id
    contact_no = request.data.get('contact_no')
    contact_no = '8801' + contact_no[-9:]
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
# @deco.get_permission(['delete_customer'])
def deletecustomer(request, customerid=None):
    response_data, response_message, response_successflag, response_status = ghelp().deleterecord(
        classOBJ=MODELS_USER.User,
        id=customerid,
        
    )
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)
