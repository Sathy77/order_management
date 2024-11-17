# from django.shortcuts import render, get_object_or_404
# from django.http import HttpResponse
# from django.utils import timezone
# # from weasyprint import HTML
# # from weasyprint.css import CSS
# from xhtml2pdf import pisa
# from io import BytesIO
# from helps.common.generic import Generichelps as ghelp
# from order import models as MODELS_ORDE
# from om_settings import models as MODELS_SETT
# from account import models as MODELS_ACCO
# from user import models as MODELS_USER
# from product import models as MODELS_PROD
# from django.template.loader import get_template
# from rest_framework.decorators import api_view, permission_classes
# from django.db.models import Q
# from rest_framework.permissions import IsAuthenticated

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# # @deco.get_permission(['order_report_view'])
# def get_orders_pdf(request):
#     # Filter fields for the order queryset
#     filter_fields = [
#         {'name': 'id', 'convert': None, 'replace':'id'},
#         {'name': 'customer', 'convert': None, 'replace':'user'},
#         {'name': 'customer_name', 'convert': None, 'replace':'user__name__icontains'},
#         {'name': 'customer_contact_no', 'convert': None, 'replace':'user__contact_no__icontains'},
#         {'name': 'customer_email', 'convert': None, 'replace':'user__email__icontains'},
#         {'name': 'date_from', 'convert': None, 'replace':'date__gte'},
#         {'name': 'date_to', 'convert': None, 'replace':'date__lte'},
#         {'name': 'invoice_no', 'convert': None, 'replace':'invoice_no__icontains'},
#         {'name': 'deliveryzone', 'convert': None, 'replace':'deliveryzone'},
#         {'name': 'payment_mode', 'convert': None, 'replace':'payment_mode'},
#         {'name': 'product_cost', 'convert': None, 'replace':'product_cost'},
#         {'name': 'delivery_cost', 'convert': None, 'replace':'delivery_cost'},
#         {'name': 'coupon', 'convert': None, 'replace':'coupon'},
#         {'name': 'discount', 'convert': None, 'replace':'discount'},
#         {'name': 'free_delivery', 'convert': 'bool', 'replace':'free_delivery'},
#         {'name': 'grand_total', 'convert': None, 'replace':'grand_total'},
#         {'name': 'total_profit', 'convert': None, 'replace':'total_profit'},
#         {'name': 'order_status', 'convert': None, 'replace':'order_status__icontains'},
#         {'name': 'payment_status', 'convert': None, 'replace':'payment_status__icontains'},
#     ]

#     # Fetch orders with the applied filters
#     orders = MODELS_ORDE.Ordersummary.objects.filter(**ghelp().KWARGS(request, filter_fields))
#     time_now = timezone.now()
#     settings = MODELS_SETT.Settings.objects.first()
#     if settings and settings.logo:
#     # Convert the logo path to a full URL
#         logo_url = request.build_absolute_uri(settings.logo.url)
#     else:
#         logo_url = ''


#     context = {
#         'orders': orders,
#         'time_now': time_now,
#         'site_name': settings.company_name if settings else '',
#         'company_name': settings.company_name if settings else '',
#         'logo': logo_url,
#         'address': settings.address if settings else '',
#         'phone_number': settings.phone_number if settings else '',
#         'email': settings.email if settings else '',
#     }

#     # Render HTML template with context
#     template = get_template('order/order.html')
#     html_content = template.render(context)

#     # Use WeasyPrint to generate PDF
#     response = HttpResponse(content_type="application/pdf")
#     response['Content-Disposition'] = 'inline; filename="orders_summary.pdf"'
    
#     # Set up CSS with embedded Kalpurush font
#     css = CSS(string="""
#     @font-face {
#         font-family: 'Kalpurush';
#         src: url('font/Kalpurush.ttf') format('truetype');
#     }
#     body, p, h1, h2, h3, h4, h5, tr, td {
#         font-family: 'Kalpurush', Arial, sans-serif;
#         font-size: 12px;
#     }
#     th, h1, h2, h3, b {
#     font-family: Arial, sans-serif; /* Fallback to a font that supports bold */
#     font-weight: bold;
#     }
#     """)
    
#     HTML(string=html_content).write_pdf(response, stylesheets=[css])

#     return response

# @api_view(['GET'])
# # @permission_classes([IsAuthenticated])
# # @deco.get_permission(['customer_report_view'])
# def get_customers_pdf(request):
#     # Filter fields for the order queryset
#     filter_fields = [
#         {'name': 'id', 'convert': None, 'replace':'id'},
#         {'name': 'name', 'convert': None, 'replace':'name__icontains'},
#         {'name': 'address', 'convert': None, 'replace':'address__icontains'},
#         {'name': 'contact_no', 'convert': None, 'replace':'contact_no'},
#         {'name': 'email', 'convert': None, 'replace':'email__icontains'},
#     ]

#     KWARGS = ghelp().KWARGS(request, filter_fields)
#     KWARGS.update({'user_type': 'Customer'})
#     customers = MODELS_USER.User.objects.filter(**KWARGS)
    
#     #One sheach feild at a time 1 atribute but options will many
#     #the filter will look for the search_term in the name, contact_no, or email fields.
#     search_term = request.GET.get('search_term')
#     if search_term != None:
#         customers = customers.filter(Q(name__icontains=search_term) | Q(email__icontains=search_term) | Q(contact_no__icontains=search_term))
    
#     time_now = timezone.now()
#     settings = MODELS_SETT.Settings.objects.first()
#     if settings and settings.logo:
#     # Convert the logo path to a full URL
#         logo_url = request.build_absolute_uri(settings.logo.url)
#     else:
#         logo_url = ''


#     context = {
#         'customers': customers,
#         'time_now': time_now,
#         'site_name': settings.company_name if settings else '',
#         'company_name': settings.company_name if settings else '',
#         'logo': logo_url,
#         'address': settings.address if settings else '',
#         'phone_number': settings.phone_number if settings else '',
#         'email': settings.email if settings else '',
#     }

#     # Render HTML template with context
#     template = get_template('customer/customer.html')
#     html_content = template.render(context)

#     # Use WeasyPrint to generate PDF
#     response = HttpResponse(content_type="application/pdf")
#     response['Content-Disposition'] = 'inline; filename="customers.pdf"'
    
#     # Set up CSS with embedded Kalpurush font
#     string="""
#     @font-face {
#         font-family: 'Kalpurush';
#         src: url('font/Kalpurush.ttf') format('truetype');
#     }
#     body, p, h1, h2, h3, h4, h5, tr, td {
#         font-family: 'Kalpurush', Arial, sans-serif;
#         font-size: 12px;
#     }
#     th, h1, h2, h3, b {
#     font-family: Arial, sans-serif; /* Fallback to a font that supports bold */
#     font-weight: bold;
#     }
#     """
    
#     pisa_status = pisa.CreatePDF(html_content, dest=response)

#     # Check for errors during PDF generation
#     if pisa_status.err:
#         return HttpResponse("Error generating PDF", status=500)
#     # response = result

#     return response

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# # @deco.get_permission(['transection_report_view'])
# def get_transections_pdf(request):
#     # Filter fields for the order queryset
#     filter_fields = [
#         {'name': 'id', 'convert': None, 'replace':'id'},

#         {'name': 'date_from', 'convert': None, 'replace':'date__gte'},
#         {'name': 'date_to', 'convert': None, 'replace':'date__lte'},

#         {'name': 'amount_from', 'convert': None, 'replace':'amount__gte'},
#         {'name': 'amount_to', 'convert': None, 'replace':'amount__lte'},

#         {'name': 'ordersummary', 'convert': None, 'replace':'ordersummary'},
#         {'name': 'reference', 'convert': None, 'replace':'reference__icontains'},
#         {'name': 'date', 'convert': None, 'replace':'date'},
#         {'name': 'amount', 'convert': None, 'replace':'amount__icontains'}
#     ]
#     transections = MODELS_ACCO.Transection.objects.filter(**ghelp().KWARGS(request, filter_fields))
#     search_term = request.GET.get('search_term')
#     heads = request.GET.get('head')
#     expense_total_amount = 0
#     income_total_amount = 0
#     if search_term == 'expense':
#         transections = MODELS_ACCO.Transection.objects.filter(income__isnull=True)
#         if not heads:
#             for transection in transections:
#                 amount = transection.amount
#                 expense_total_amount += amount
    
#     elif search_term == 'income':
#         transections = MODELS_ACCO.Transection.objects.filter(expense__isnull=True)
#         if not heads:
#             for transection in transections:
#                 amount = transection.amount
#                 income_total_amount += amount

#     if heads:
#         transections = transections.filter(Q(income__title__icontains=heads) | Q(expense__title__icontains=heads))  
#         if search_term == 'expense':
#             for transection in transections:
#                 amount = transection.amount
#                 expense_total_amount += amount
#         elif search_term == 'income':
#             for transection in transections:
#                 amount = transection.amount
#                 income_total_amount += amount

#     if not search_term :
#         if not heads:
#             expense_transections = MODELS_ACCO.Transection.objects.filter(income__isnull=True)
#             for expense_transection in expense_transections:
#                 amount = expense_transection.amount
#                 expense_total_amount += amount
#             income_transections = MODELS_ACCO.Transection.objects.filter(expense__isnull=True)
#             for income_transection in income_transections:
#                 amount = income_transection.amount
#                 income_total_amount += amount

#     time_now = timezone.now()
#     settings = MODELS_SETT.Settings.objects.first()
#     if settings and settings.logo:
#     # Convert the logo path to a full URL
#         logo_url = request.build_absolute_uri(settings.logo.url)
#     else:
#         logo_url = ''


#     context = {
#         'transections': transections,
#         'time_now': time_now,
#         'site_name': settings.company_name if settings else '',
#         'company_name': settings.company_name if settings else '',
#         'logo': logo_url,
#         'address': settings.address if settings else '',
#         'phone_number': settings.phone_number if settings else '',
#         'email': settings.email if settings else '',
#         'income_total_amount': income_total_amount,
#         'expense_total_amount': expense_total_amount,
#     }

#     # Render HTML template with context
#     template = get_template('transection/transection.html')
#     html_content = template.render(context)

#     # Use WeasyPrint to generate PDF
#     response = HttpResponse(content_type="application/pdf")
#     response['Content-Disposition'] = 'inline; filename="transections.pdf"'
    
#     # Set up CSS with embedded Kalpurush font
#     css = CSS(string="""
#     @font-face {
#         font-family: 'Kalpurush';
#         src: url('font/Kalpurush.ttf') format('truetype');
#     }
#     body, p, h1, h2, h3, h4, h5, tr, td {
#         font-family: 'Kalpurush', Arial, sans-serif;
#         font-size: 12px;
#         font-weight: bold;
#     }
#     th, h1, h2, h3, b {
#     font-family: Arial, sans-serif; /* Fallback to a font that supports bold */
#     font-weight: bold;
#     }
#     """)
    
#     HTML(string=html_content).write_pdf(response, stylesheets=[css])

#     return response

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# # @deco.get_permission(['product_report_view'])
# def get_products_pdf(request):
#     # Filter fields for the order queryset
#     filter_fields = [
#         {'name': 'id', 'convert': None, 'replace':'id'},
#         # {'name': 'name', 'convert': None, 'replace':'name__icontains'},
#         {'name': 'weight', 'convert': None, 'replace':'weight'},
#         {'name': 'quntity', 'convert': None, 'replace':'quntity'},
#         # {'name': 'costprice', 'convert': None, 'replace':'costprice'},
#         # {'name': 'mrpprice', 'convert': None, 'replace':'mrpprice'}
#     ]

#     products = MODELS_PROD.Product.objects.filter(**ghelp().KWARGS(request, filter_fields))

#     #One sheach feild at a time 1 atribute but options will many
#     #the filter will look for the search_term in the name, contact_no, or email fields.
#     search_term = request.GET.get('search_term')
#     if search_term != None:
#         products = products.filter(Q(name__icontains=search_term) | Q(costprice__icontains=search_term) | Q(mrpprice__icontains=search_term))
  

#     time_now = timezone.now()
#     settings = MODELS_SETT.Settings.objects.first()
#     if settings and settings.logo:
#     # Convert the logo path to a full URL
#         logo_url = request.build_absolute_uri(settings.logo.url)
#     else:
#         logo_url = ''


#     context = {
#         'products': products,
#         'time_now': time_now,
#         'site_name': settings.company_name if settings else '',
#         'company_name': settings.company_name if settings else '',
#         'logo': logo_url,
#         'address': settings.address if settings else '',
#         'phone_number': settings.phone_number if settings else '',
#         'email': settings.email if settings else '',
#     }

#     # Render HTML template with context
#     template = get_template('product/product.html')
#     html_content = template.render(context)

#     # Use WeasyPrint to generate PDF
#     response = HttpResponse(content_type="application/pdf")
#     response['Content-Disposition'] = 'inline; filename="transections.pdf"'
    
#     # Set up CSS with embedded Kalpurush font
#     css = CSS(string="""
#     @font-face {
#         font-family: 'Kalpurush';
#         src: url('font/Kalpurush.ttf') format('truetype');
#     }
#     body, p, h1, h2, h3, h4, h5, tr, td {
#         font-family: 'Kalpurush', Arial, sans-serif;
#         font-size: 12px;
#         font-weight: bold;
#     }
#     th, h1, h2, h3, b {
#     font-family: Arial, sans-serif; /* Fallback to a font that supports bold */
#     font-weight: bold;
#     }
#     """)
    
#     HTML(string=html_content).write_pdf(response, stylesheets=[css])

#     return response

