from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from helps.decorators.decorator import CommonDecorator as deco
from account import models as MODELS_ACCO
from account.serializer.GET import serializers as GET_SRLZER_ACCO
from account.serializer.POST import serializers as POST_SRLZER_ACCO
# from payroll.serializer.POST import serializers as PSRLZER_PAYR
from helps.common.generic import Generichelps as ghelp
from rest_framework.response import Response
from helps.choice import common as CHOICE
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getincomes(request):
    filter_fields = [
        {'name': 'id', 'convert': None, 'replace':'id'},
        {'name': 'name', 'convert': None, 'replace':'name__icontains'},
        {'name': 'balance', 'convert': None, 'replace':'balance'}
    ]
    incomes = MODELS_ACCO.Income.objects.filter(**ghelp().KWARGS(request, filter_fields))

    column_accessor = request.GET.get('column_accessor')
    if column_accessor: incomes = incomes.order_by(column_accessor)
    
    total_count = incomes.count()
    page = int(request.GET.get('page')) if request.GET.get('page') else 1
    page_size = int(request.GET.get('page_size')) if request.GET.get('page_size') else 10
    if page and page_size: incomes=incomes[(page-1)*page_size:page*page_size]

    incomeserializers = GET_SRLZER_ACCO.Incomeserializer(incomes, many=True)
    return Response({'data': {
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'result': incomeserializers.data
    }, 'message': [], 'status': 'success'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@deco.get_permission(['add income'])
def addincome(request):
    requestdata = request.data.copy()
    userid = request.user.id
    extra_fields = {}
    if userid: extra_fields.update({'created_by': request.user.id, 'updated_by': request.user.id})
    required_fields = ['title', 'balance']
    # fields_regex = [{'field': 'date', 'type': 'date'}, {'field': 'in_time', 'type': 'time'}, {'field': 'out_time', 'type': 'time'}]
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(
        classOBJ=MODELS_ACCO.Income, 
        Serializer=POST_SRLZER_ACCO.Incomeserializer, 
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
def updateincome(request, incomeid=None):
    userid = request.user.id
    extra_fields = {}
    if userid: extra_fields.update({'updated_by': userid})
    response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
        classOBJ=MODELS_ACCO.Income, 
        Serializer=POST_SRLZER_ACCO.Incomeserializer, 
        id=incomeid,
        data=request.data,
        extra_fields=extra_fields
    )
    response_data = response_data.data if response_successflag == 'success' else {}
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def deleteincome(request, incomeid=None):
    response_data, response_message, response_successflag, response_status = ghelp().deleterecord(
        classOBJ=MODELS_ACCO.Income,
        id=incomeid
    )
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Single Permission Details', 'all'])
def getexpenses(request):
    filter_fields = [
        {'name': 'id', 'convert': None, 'replace':'id'},
        {'name': 'name', 'convert': None, 'replace':'name__icontains'},
        {'name': 'balance', 'convert': None, 'replace':'balance'}
    ]
    expenses = MODELS_ACCO.Expense.objects.filter(**ghelp().KWARGS(request, filter_fields))

    column_accessor = request.GET.get('column_accessor')
    if column_accessor: expenses = expenses.order_by(column_accessor)
    
    total_count = expenses.count()
    page = int(request.GET.get('page')) if request.GET.get('page') else 1
    page_size = int(request.GET.get('page_size')) if request.GET.get('page_size') else 10
    if page and page_size: expenses=expenses[(page-1)*page_size:page*page_size]

    expenseserializers = GET_SRLZER_ACCO.Expenseserializer(expenses, many=True)
    return Response({'data': {
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'result': expenseserializers.data
    }, 'message': [], 'status': 'success'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Account'])
def addexpense(request):
    requestdata = request.data.copy()
    userid = request.user.id
    extra_fields = {}
    if userid: extra_fields.update({'created_by': request.user.id, 'updated_by': request.user.id})
    required_fields = ['title', 'balance']
    # fields_regex = [{'field': 'date', 'type': 'date'}, {'field': 'in_time', 'type': 'time'}, {'field': 'out_time', 'type': 'time'}]
    response_data, response_message, response_successflag, response_status = ghelp().addtocolass(
        classOBJ=MODELS_ACCO.Expense, 
        Serializer=POST_SRLZER_ACCO.Expenseserializer, 
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
def updateexpense(request, expenseid=None):
    userid = request.user.id
    extra_fields = {}
    if userid: extra_fields.update({'updated_by': userid})
    response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
        classOBJ=MODELS_ACCO.Income, 
        Serializer=POST_SRLZER_ACCO.Incomeserializer, 
        id=expenseid,
        data=request.data,
        extra_fields=extra_fields
    )
    response_data = response_data.data if response_successflag == 'success' else {}
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['Get Permission list Details', 'all'])
def deleteexpense(request, expenseid=None):
    response_data, response_message, response_successflag, response_status = ghelp().deleterecord(
        classOBJ=MODELS_ACCO.Expense,
        id=expenseid
    )
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['coco'])
def addtransectionincome(request):
    response_data = {}
    response_message = []
    response_successflag = 'error'
    response_status = status.HTTP_400_BAD_REQUEST

    userid = request.user.id
    requestdata = request.data.copy()
    incomeid = requestdata.get('income')

    if incomeid:
        income = MODELS_ACCO.Income.objects.filter(id=incomeid)
        if income.exists():
            income_balance = income.first().balance
            amount = requestdata.get('amount')
            if amount:
                income_balance = income_balance + amount
            else :
                amount = 0
                income_balance = income_balance + amount
            
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

            response_successflag = responsesuccessflag

            if response_successflag == 'success':
                required_fields = ['income','date', 'amount']
                fields_regex = [{'field': 'date', 'type': 'date'}]
                response_data, response_message, response_successflag, response_status = ghelp().addtocolass(
                    classOBJ=MODELS_ACCO.Transectionincome, 
                    Serializer=POST_SRLZER_ACCO.Transectionincomeserializer, 
                    data=requestdata, 
                    unique_fields=[], 
                    fields_regex=fields_regex, 
                    required_fields=required_fields
                )
                if response_data: response_data = response_data.data
        else: response_message.append('Income id is invalid!')
    else: response_message.append('Income id is required!')
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['get company info', 'all'])
def addtransectionexpense(request):
    response_data = {}
    response_message = []
    response_successflag = 'error'
    response_status = status.HTTP_400_BAD_REQUEST

    userid = request.user.id
    requestdata = request.data.copy()
    expenseid = requestdata.get('expense')

    if expenseid:
        expense = MODELS_ACCO.Expense.objects.filter(id=expenseid)
        if expense.exists():
            expense_balance = expense.first().balance
            amount = requestdata.get('amount')
            if amount:
                expense_balance = expense_balance + amount
            else :
                amount = 0
                expense_balance = expense_balance + amount
            
            extra_fields = {}
            if userid: extra_fields.update({'updated_by': userid})
            prepare_data={'balance': expense_balance}
            responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().updaterecord(
                classOBJ=MODELS_ACCO.Expense, 
                Serializer=POST_SRLZER_ACCO.Expenseserializer, 
                id=expenseid,
                data=prepare_data,
                extra_fields=extra_fields
            )
            response_data = responsedata.data if responsesuccessflag == 'success' else {}

            response_successflag = responsesuccessflag

            if response_successflag == 'success':
                required_fields = ['expense','date', 'amount']
                fields_regex = [{'field': 'date', 'type': 'date'}]
                response_data, response_message, response_successflag, response_status = ghelp().addtocolass(
                    classOBJ=MODELS_ACCO.Transectionexpense, 
                    Serializer=POST_SRLZER_ACCO.Transectionexpenseserializer, 
                    data=requestdata, 
                    unique_fields=[], 
                    fields_regex=fields_regex, 
                    required_fields=required_fields
                )
                if response_data: response_data = response_data.data
        else: response_message.append('Income id is invalid!')
    else: response_message.append('Income id is required!')
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)