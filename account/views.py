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
from django.db.models import Q





@api_view(['GET'])
@permission_classes([IsAuthenticated])
@deco.get_permission(['view_income'])
def getincomes(request):
    if not MODELS_ACCO.Income.objects.all().exists():
        userid = request.user.id
        extra_fields = {}
        prepare_data={'title': 'Sales', 'balance': 0}
        if userid: extra_fields.update({'created_by': request.user.id, 'updated_by': request.user.id})
        required_fields = ['title', 'balance']
        ghelp().addtocolass(
        classOBJ=MODELS_ACCO.Income, 
        Serializer=POST_SRLZER_ACCO.Incomeserializer, 
        data=prepare_data, 
        unique_fields=[], 
        extra_fields=extra_fields, 
        required_fields=required_fields
    )
    filter_fields = [
        {'name': 'id', 'convert': None, 'replace':'id'},
        {'name': 'title', 'convert': None, 'replace':'title__icontains'},
        {'name': 'balance', 'convert': None, 'replace':'balance'}
    ]
    incomes = MODELS_ACCO.Income.objects.filter(**ghelp().KWARGS(request, filter_fields))
    
    incomes, total_count, page, page_size = ghelp().getPaginatedData(request, incomes)
    incomeserializers = GET_SRLZER_ACCO.Incomeserializer(incomes, many=True)
    return Response({'data': {
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'results': incomeserializers.data
    }, 'message': [], 'status': 'success'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@deco.get_permission(['create_income'])
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
@deco.get_permission(['edit_income'])
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
@deco.get_permission(['delete_income'])
def deleteincome(request, incomeid=None):
    response_data, response_message, response_successflag, response_status = ghelp().deleterecord(
        classOBJ=MODELS_ACCO.Income,
        id=incomeid
    )
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@deco.get_permission(['view_expense'])
def getexpenses(request):
    if not MODELS_ACCO.Expense.objects.all().exists():
        userid = request.user.id
        extra_fields = {}
        prepare_data={'title': 'Purchase', 'balance': 0}
        if userid: extra_fields.update({'created_by': request.user.id, 'updated_by': request.user.id})
        required_fields = ['title', 'balance']
        ghelp().addtocolass(
        classOBJ=MODELS_ACCO.Expense, 
        Serializer=POST_SRLZER_ACCO.Expenseserializer, 
        data=prepare_data, 
        unique_fields=[], 
        extra_fields=extra_fields, 
        required_fields=required_fields
    )
    filter_fields = [
        {'name': 'id', 'convert': None, 'replace':'id'},
        {'name': 'title', 'convert': None, 'replace':'title__icontains'},
        {'name': 'balance', 'convert': None, 'replace':'balance'}
    ]
    expenses = MODELS_ACCO.Expense.objects.filter(**ghelp().KWARGS(request, filter_fields))

    expenses, total_count, page, page_size = ghelp().getPaginatedData(request, expenses)

    expenseserializers = GET_SRLZER_ACCO.Expenseserializer(expenses, many=True)
    return Response({'data': {
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'results': expenseserializers.data
    }, 'message': [], 'status': 'success'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@deco.get_permission(['create_expense'])
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
@deco.get_permission(['edit_expense'])
def updateexpense(request, expenseid=None):
    userid = request.user.id
    extra_fields = {}
    if userid: extra_fields.update({'updated_by': userid})
    response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
        classOBJ=MODELS_ACCO.Expense, 
        Serializer=POST_SRLZER_ACCO.Expenseserializer, 
        id=expenseid,
        data=request.data,
        extra_fields=extra_fields
    )
    response_data = response_data.data if response_successflag == 'success' else {}
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@deco.get_permission(['delete_expense'])
def deleteexpense(request, expenseid=None):
    response_data, response_message, response_successflag, response_status = ghelp().deleterecord(
        classOBJ=MODELS_ACCO.Expense,
        id=expenseid
    )
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@deco.get_permission(['view_transection'])
def gettransections(request):
    filter_fields = [
        {'name': 'id', 'convert': None, 'replace':'id'},

        {'name': 'date_from', 'convert': None, 'replace':'date__gte'},
        {'name': 'date_to', 'convert': None, 'replace':'date__lte'},

        {'name': 'amount_from', 'convert': None, 'replace':'amount__gte'},
        {'name': 'amount_to', 'convert': None, 'replace':'amount__lte'},

        {'name': 'ordersummary', 'convert': None, 'replace':'ordersummary'},
        {'name': 'reference', 'convert': None, 'replace':'reference__icontains'},
        {'name': 'date', 'convert': None, 'replace':'date'},
        {'name': 'amount', 'convert': None, 'replace':'amount__icontains'}
    ]
    transections = MODELS_ACCO.Transection.objects.filter(**ghelp().KWARGS(request, filter_fields))
    search_term = request.GET.get('search_term')
    heads = request.GET.get('head')
    order = request.GET.get('order')
    
    if search_term == 'expense':
        transections = MODELS_ACCO.Transection.objects.filter(income__isnull=True)
    
    elif search_term == 'income':
        transections = MODELS_ACCO.Transection.objects.filter(expense__isnull=True)

    if order == 'all':
        transections = MODELS_ACCO.Transection.objects.filter(ordersummary__isnull=False)

    if heads:
        transections = transections.filter(Q(income__title__icontains=heads) | Q(expense__title__icontains=heads))

    transections, total_count, page, page_size = ghelp().getPaginatedData(request, transections)

    transectionserializers = GET_SRLZER_ACCO.Transectionserializer(transections, many=True)
    return Response({'data': {
        'count': total_count,
        'page': page,
        'page_size': page_size,
        'results': transectionserializers.data
    }, 'message': [], 'status': 'success'}, status=status.HTTP_200_OK)
    
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@deco.get_permission(['create_transection'])
def addtransection(request):
    response_data = {}
    response_message = []
    response_successflag = 'error'
    response_status = status.HTTP_400_BAD_REQUEST

    userid = request.user.id
    requestdata = request.data.copy()
    incomeid = requestdata.get('income')
    expenseid = requestdata.get('expense')

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
        else: response_message.append('Income id is invalid!')
    else: 
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
            else: response_message.append('Income id is invalid!')
        else: response_message.append('Income or Expense id is required!')

    if response_successflag == 'success':
        required_fields = ['date', 'amount']
        fields_regex = [{'field': 'date', 'type': 'date'}]
        response_data, response_message, response_successflag, response_status = ghelp().addtocolass(
            classOBJ=MODELS_ACCO.Transection, 
            Serializer=POST_SRLZER_ACCO.Transectionserializer, 
            data=requestdata, 
            unique_fields=[], 
            fields_regex=fields_regex, 
            required_fields=required_fields
        )
        if response_data: response_data = response_data.data
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@deco.get_permission(['edit_transection'])
def updatetransection(request, transectionid=None):
    response_data = {}
    response_message = []
    response_successflag = 'error'
    response_status = status.HTTP_400_BAD_REQUEST

    userid = request.user.id
    requestdata = request.data.copy()

    new_income = requestdata.get('income')
    new_expense = requestdata.get('expense')
    if new_income: requestdata.update({'expense': None})
    if new_expense: requestdata.update({'income': None})
    
    new_amount = requestdata.get('amount')

    transection = MODELS_ACCO.Transection.objects.filter(id=transectionid)
    previous_amount = transection.first().amount
    if transection.exists():
        previous_incomeid = transection.first().income.id if transection.first() and transection.first().income else None
        previous_expenseid = transection.first().expense.id if transection.first() and transection.first().expense else None
        if previous_incomeid:
            if new_income: 
                # requestdata.update({'expense': None})  
                amount = previous_amount - new_amount
                income = MODELS_ACCO.Income.objects.filter(id=previous_incomeid) 
                balance = income.first().balance
                balance = balance - amount
                response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
                classOBJ=MODELS_ACCO.Income, 
                Serializer=POST_SRLZER_ACCO.Incomeserializer, 
                id=previous_incomeid,
                data={'balance':balance},
                )
            else: 
                amount = requestdata.get('amount')
                income = MODELS_ACCO.Income.objects.filter(id=previous_incomeid) 
                balance = income.first().balance
                balance = balance - amount
                response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
                classOBJ=MODELS_ACCO.Income, 
                Serializer=POST_SRLZER_ACCO.Incomeserializer, 
                id=previous_incomeid,
                data={'balance':balance},
                )
                if new_expense:
                    expense = MODELS_ACCO.Expense.objects.filter(id=new_expense)
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
                            id=new_expense,
                            data=prepare_data,
                            extra_fields=extra_fields
                        )
                        response_data = responsedata.data if responsesuccessflag == 'success' else {}
                        response_successflag = responsesuccessflag
                    else: response_message.append('Expense id is not valid!')

        elif previous_expenseid:
            if new_expense: 
                # requestdata.update({'income': None})
                amount = previous_amount - new_amount
                expense = MODELS_ACCO.Expense.objects.filter(id=previous_expenseid) 
                balance = expense.first().balance
                balance = balance - amount
                response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
                classOBJ=MODELS_ACCO.Expense, 
                Serializer=POST_SRLZER_ACCO.Expenseserializer, 
                id=previous_expenseid,
                data={'balance':balance},
                )
            else:
                amount = requestdata.get('amount')
                expense = MODELS_ACCO.Expense.objects.filter(id=previous_expenseid)
                balance = expense.first().balance
                balance = balance - amount
                response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
                classOBJ=MODELS_ACCO.Expense, 
                Serializer=POST_SRLZER_ACCO.Expenseserializer, 
                id=previous_expenseid,
                data={'balance':balance},
                )
                if new_income:
                    income = MODELS_ACCO.Income.objects.filter(id=new_income)
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
                            id=new_income,
                            data=prepare_data,
                            extra_fields=extra_fields
                        )
                        response_data = responsedata.data if responsesuccessflag == 'success' else {}
                        response_successflag = responsesuccessflag
                    else: response_message.append('Income id is invalid!')
    else: response_message.append('transection doesn\'t exist!')

    if response_successflag == 'success':
        fields_regex = [{'field': 'date', 'type': 'date'}]
        response_data, response_message, response_successflag, response_status = ghelp().updaterecord(
        classOBJ=MODELS_ACCO.Transection, 
        Serializer=POST_SRLZER_ACCO.Transectionserializer, 
        fields_regex=fields_regex,
        id=transectionid,
        data=requestdata,
        )
        if isinstance(response_data, POST_SRLZER_ACCO.Transectionserializer):
            response_data = response_data.data
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)
##    
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# # @deco.get_permission(['add transection expense', 'all'])
# def addtransectionexpense(request):
#     response_data = {}
#     response_message = []
#     response_successflag = 'error'
#     response_status = status.HTTP_400_BAD_REQUEST

#     userid = request.user.id
#     requestdata = request.data.copy()
#     expenseid = requestdata.get('expense')

#     if expenseid:
#         expense = MODELS_ACCO.Expense.objects.filter(id=expenseid)
#         if expense.exists():
#             expense_balance = expense.first().balance
#             amount = requestdata.get('amount')
#             if amount:
#                 expense_balance = expense_balance + amount
#             else :
#                 amount = 0
#                 expense_balance = expense_balance + amount
            
#             extra_fields = {}
#             if userid: extra_fields.update({'updated_by': userid})
#             prepare_data={'balance': expense_balance}
#             responsedata, responsemessage, responsesuccessflag, responsestatus = ghelp().updaterecord(
#                 classOBJ=MODELS_ACCO.Expense, 
#                 Serializer=POST_SRLZER_ACCO.Expenseserializer, 
#                 id=expenseid,
#                 data=prepare_data,
#                 extra_fields=extra_fields
#             )
#             response_data = responsedata.data if responsesuccessflag == 'success' else {}

#             response_successflag = responsesuccessflag

#             if response_successflag == 'success':
#                 required_fields = ['expense','date', 'amount']
#                 fields_regex = [{'field': 'date', 'type': 'date'}]
#                 response_data, response_message, response_successflag, response_status = ghelp().addtocolass(
#                     classOBJ=MODELS_ACCO.Transectionexpense, 
#                     Serializer=POST_SRLZER_ACCO.Transectionexpenseserializer, 
#                     data=requestdata, 
#                     unique_fields=[], 
#                     fields_regex=fields_regex, 
#                     required_fields=required_fields
#                 )
#                 if response_data: response_data = response_data.data
#         else: response_message.append('Income id is invalid!')
#     else: response_message.append('Income id is required!')
#     return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

