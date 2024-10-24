from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from product import models as MODELS_PROD
from product.serializer.GET import serializers as GET_SRLZER_PROD
from product.serializer.POST import serializers as POST_SRLZER_PROD
from helps.common.generic import Generichelps as ghelp
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_nested_forms.utils import NestedForm
from django.db.models import Q

# Create your views here.

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getproducts_noauth(request):
    filter_fields = [
        {'name': 'id', 'convert': None, 'replace':'id'},
        # {'name': 'name', 'convert': None, 'replace':'name__icontains'},
        {'name': 'weight', 'convert': None, 'replace':'weight'},
        {'name': 'quntity', 'convert': None, 'replace':'quntity'},
        # {'name': 'costprice', 'convert': None, 'replace':'costprice'},
        # {'name': 'mrpprice', 'convert': None, 'replace':'mrpprice'}
    ]

    products = MODELS_PROD.Product.objects.filter(**ghelp().KWARGS(request, filter_fields))

    #One sheach feild at a time 1 atribute but options will many
    #the filter will look for the search_term in the name, contact_no, or email fields.
    search_term = request.GET.get('search_term')
    if search_term != None:
        products = products.filter(Q(name__icontains=search_term) | Q(costprice__icontains=search_term) | Q(mrpprice__icontains=search_term))

    products, total_count, page, page_size = ghelp().getPaginatedData(request, products)

    productserializers = GET_SRLZER_PROD.Productserializer(products, many=True)
    return Response({'data': {
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'results': productserializers.data
    }, 'message': [], 'status': 'success'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['get company info', 'all'])
def addproduct(request):
    requestdata = dict(request.data)
    requestdata.update({'abcdef[abcdef]': ['abcdef']})
    options = {'allow_blank': True, 'allow_empty': False}
    form = NestedForm(requestdata, **options)
    form.is_nested(raise_exception=True)
    requestdata = ghelp().prepareData(form.data, 'product')
    userid = request.user.id
    extra_fields = {}
    if userid: extra_fields.update({'created_by': request.user.id, 'updated_by': request.user.id})
    required_fields = ['name', 'photo', 'weight', 'quntity', 'costprice', 'mrpprice']
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(
        classOBJ=MODELS_PROD.Product, 
        Serializer=POST_SRLZER_PROD.Productserializer, 
        data=requestdata, 
        unique_fields=[], 
        extra_fields=extra_fields, 
        required_fields=required_fields
    )
    if response_data: response_data = response_data.data
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def updateproduct(request, productid=None):
    requestdata = dict(request.data)
    requestdata.update({'abcdef[abcdef]': ['abcdef']})
    options = {'allow_blank': True, 'allow_empty': False}
    form = NestedForm(requestdata, **options)
    form.is_nested(raise_exception=True)
    requestdata = ghelp().prepareData(form.data, 'product')
    userid = request.user.id
    extra_fields = {}
    if userid: extra_fields.update({'updated_by': userid})
    allowed_fields=['name', 'photo', 'weight', 'quntity', 'costprice', 'mrpprice']
    static_fields = ['photo']
    response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
        classOBJ=MODELS_PROD.Product, 
        Serializer=POST_SRLZER_PROD.Productserializer, 
        id=productid, 
        data=requestdata,
        allowed_fields=allowed_fields,
        # fields_regex=fields_regex,
        static_fields=static_fields
    )
    response_data = response_data.data if response_successflag == 'success' else {}
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def deleteproduct(request, productid=None):
    response_data, response_message, response_successflag, response_status = ghelp().deleterecord(
        classOBJ=MODELS_PROD.Product,
        id=productid,
    )
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getproducts_auth(request):
    filter_fields = [
        {'name': 'id', 'convert': None, 'replace':'id'},
        # {'name': 'name', 'convert': None, 'replace':'name__icontains'},
        {'name': 'weight', 'convert': None, 'replace':'weight'},
        {'name': 'quntity', 'convert': None, 'replace':'quntity'},
        # {'name': 'costprice', 'convert': None, 'replace':'costprice'},
        # {'name': 'mrpprice', 'convert': None, 'replace':'mrpprice'}
    ]

    products = MODELS_PROD.Product.objects.filter(**ghelp().KWARGS(request, filter_fields))

    #One sheach feild at a time 1 atribute but options will many
    #the filter will look for the search_term in the name, contact_no, or email fields.
    search_term = request.GET.get('search_term')
    if search_term != None:
        products = products.filter(Q(name__icontains=search_term) | Q(costprice__icontains=search_term) | Q(mrpprice__icontains=search_term))

    products, total_count, page, page_size = ghelp().getPaginatedData(request, products)

    productserializers = GET_SRLZER_PROD.Productserializer(products, many=True)
    return Response({'data': {
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'results': productserializers.data
    }, 'message': [], 'status': 'success'}, status=status.HTTP_200_OK)