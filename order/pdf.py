from django.views.generic import View
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
from order import models as MODELS_ORDE # Replace 'your_app' with your actual app name
import os

class OrderSummaryPDFView(View):
    def get(self, request, *args, **kwargs):
        # Fetch the orders from the database
        orders = MODELS_ORDE.Ordersummary.objects.filter(invoice_no__isnull=False)
        
        # Prepare data for the template
        context = {
            'orders': orders,
        }
        
        # Load the template and render it with context
        template_path = 'pdf_templates/order_summary.html'  
        template = get_template(template_path)
        html = template.render(context)
        
        # Create a response object to hold the PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="order_summary_report.pdf"'

        # Generate the PDF
        pisa_status = pisa.CreatePDF(html, dest=response)
        
        # If there's an error, show it in plain text
        if pisa_status.err:
            return HttpResponse('We had some errors generating the PDF <pre>' + html + '</pre>')
        
        return response