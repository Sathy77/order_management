from django.shortcuts import render
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, F
from rest_framework.response import Response
from account import models as MODELS_ACCO
from zone import models as MODELS_ZONE
from order import models as MODELS_ORDE
from product import models as MODELS_PROD

# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['view_monthly_sales_amount'])
def getmonthlysalesamount (request):
    response_data = []
    response_message = []
    response_successflag = 'success'
    response_status = status.HTTP_200_OK

    current_month = timezone.now().month
    current_year = timezone.now().year
    for i in range(12):
        monthly_transactions = MODELS_ACCO.Transection.objects.filter(date__year=current_year, date__month=current_month)
        monthly_sales_transactions = monthly_transactions.filter(income__title="Sales")
        total_sales_amount = 0
        if monthly_sales_transactions:
            for monthly_sales_transaction in monthly_sales_transactions:
                amount =0
                amount = monthly_sales_transaction.amount
                total_sales_amount= total_sales_amount + amount
            per_month={'year': current_year, 'month': current_month, 'total_sales_amount': total_sales_amount}
            response_data.append(per_month)
        else: 
            per_month={'year': current_year, 'month': current_month, 'total_sales_amount': total_sales_amount}
            response_data.append(per_month)
        current_month -=1
        if current_month == 0:
            current_month = 12
            current_year -= 1
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['view_monthly_profit'])
def getmonthlyprofit (request):
    response_data = []
    response_message = []
    response_successflag = 'success'
    response_status = status.HTTP_200_OK

    current_month = timezone.now().month
    current_year = timezone.now().year
    for i in range(12):
        monthly_transactions = MODELS_ACCO.Transection.objects.filter(date__year=current_year, date__month=current_month)
        monthly_income_transactions = monthly_transactions.filter(expense__isnull=True)
        monthly_expense_transactions = monthly_transactions.filter(income__isnull=True)
        total_income_amount = 0
        total_expense_amount = 0
        profit = 0
        if monthly_transactions:
            for monthly_income_transaction in monthly_income_transactions:
                amount =0
                amount = monthly_income_transaction.amount
                total_income_amount= total_income_amount + amount
            for monthly_expense_transaction in monthly_expense_transactions:
                amount =0
                amount = monthly_expense_transaction.amount
                total_expense_amount= total_expense_amount + amount
            
            profit = total_income_amount - total_expense_amount
            per_month={'year': current_year, 'month': current_month, 'profit': profit}
            response_data.append(per_month)
        else: 
            per_month={'year': current_year, 'month': current_month, 'profit': profit}
            response_data.append(per_month)
        current_month -=1
        if current_month == 0:
            current_month = 12
            current_year -= 1
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['view_monthly_location_wise_sale'])
def getmonthlylocationwisesale (request):
    response_data = []
    response_message = []
    response_successflag = 'success'
    response_status = status.HTTP_200_OK

    zonewisetransections = []
    deliveryzones = MODELS_ZONE.Deliveryzone.objects.all()
    
    if deliveryzones:
        for deliveryzone in deliveryzones:
            deliveryzoneid = deliveryzone.id
            zonename = deliveryzone.name
            zonewiseorders = MODELS_ORDE.Ordersummary.objects.filter(deliveryzone = deliveryzoneid)
            
            zonewiseorderids = list(set([zonewiseorder.id for zonewiseorder in zonewiseorders])) ## list of id then covert it set because ignor duplicate value
            zonewisetransections = MODELS_ACCO.Transection.objects.filter(ordersummary__in=zonewiseorderids) # filter with a list od id
            zone = []
            current_month = timezone.now().month
            current_year = timezone.now().year

            if zonewisetransections:
                for i in range(12):
                    monthly_transactions = zonewisetransections.filter(date__year=current_year, date__month=current_month)
                    monthly_sales_transactions = monthly_transactions.filter(income__title="Sales")
                    total_sales_amount = 0
                    if monthly_sales_transactions:
                        for monthly_sales_transaction in monthly_sales_transactions:
                            amount =0
                            amount = monthly_sales_transaction.amount
                            total_sales_amount= total_sales_amount + amount
                        per_month={ 'year': current_year, 'month': current_month, 'total_sales_amount': total_sales_amount}
                        zone.append(per_month)
                    else: 
                        per_month={'year': current_year, 'month': current_month, 'total_sales_amount': total_sales_amount}
                        zone.append(per_month)   
                    current_month -=1
                    if current_month == 0:
                        current_month = 12
                        current_year -= 1 
                per_month={'zone_name': zonename, 'sales': zone}
                response_data.append(per_month)
            else: 
                per_month={'zone_name': zonename, 'sales': zone}
                response_data.append(per_month)
                    
    return Response({'data': response_data, 'message': response_message, 'status': response_successflag}, status=response_status)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @deco.get_permission(['view_monthly_item_wise_sales'])
def getmonthlyitemwisesales(request):
    response_data = []
    response_message = []
    response_successflag = 'success'
    response_status = status.HTTP_200_OK

    current_month = timezone.now().month
    current_year = timezone.now().year
    # requestdata = request.data.copy()
    heads = request.GET.get('head') 
    print(heads)

    if heads in ['quantity', 'Quantity']:
        # Fetch top 10 products by sales quantity for the current month and specified order statuses
        for i in range(12):
            product_data=[]
            top_products = (
                MODELS_ORDE.Orderitems.objects
                .filter(
                    ordersummary__date__month=current_month,
                    ordersummary__date__year=current_year,
                    ordersummary__order_status__in=["Pending", "On Process", "Hand over to courier", "Delivered"]
                )
                .values('product__name')  # Group by product name
                .annotate(total_quantity=Sum('order_quantity'))  # Calculate total quantity per product
                .order_by('-total_quantity')[:10]  # Get top 10
            )

            # Check if any results are returned
            if not top_products:
                product_ = {
                        "product_name": "No products found for the current month ",
                        "total_quantity": 0
                    }
                product_data.append(product_)
            else:
                # Format the result data
                for product in top_products:
                    product_ = {
                        "product_name": product['product__name'],
                        "total_quantity": product['total_quantity']
                    }
                    product_data.append(product_)
            data = {
                    "year": current_year,
                    "month": current_month,
                    "product_data": product_data,
                }
            response_data.append(data)
            current_month -=1
            if current_month == 0:
                current_month = 12
                current_year -= 1 
    
    if heads in ['Selas', 'selas']:
        for i in range(12):
            product_data=[]
            top_products = (
                MODELS_ORDE.Orderitems.objects
                .filter(
                    ordersummary__date__month=current_month,
                    ordersummary__date__year=current_year,
                    ordersummary__order_status__in=["Pending", "On Process", "Hand over to courier", "Delivered"]
                )
                .values('product__name')  # Group by product name
                .annotate(total_sales=Sum(F('order_quantity') * F('unit_mrp')) ) # Calculate total quantity per product
                .order_by('-total_sales')[:10]  # Get top 10
            )
            # Check if any results are returned
            if not top_products:
                product_ = {
                        "product_name": "No products found for the current month ",
                        "total_sales": 0
                    }
                product_data.append(product_)
            else:
                # Format the result data
                for product in top_products:
                    product_ = {
                        "product_name": product['product__name'],
                        "total_sales": product['total_sales']
                    }
                    product_data.append(product_)
            data = {
                    "year": current_year,
                    "month": current_month,
                    "product_data": product_data,
                }
            response_data.append(data)
            current_month -=1
            if current_month == 0:
                current_month = 12
                current_year -= 1

    return Response({
        "data": response_data,
        "message": response_message,
        "success_flag": response_successflag
    }, status=response_status)                  

