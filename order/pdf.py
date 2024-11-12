from order import models as MODELS_ORDE
from django.template.loader import render_to_string
from weasyprint import HTML
from django.http import HttpResponse

def generate_order_summary_pdf(request):
    # Fetch all orders (example)
    orders = MODELS_ORDE.Ordersummary.objects.all()
    
    # Render the HTML content using a Django template
    html_content = render_to_string('order_summary_pdf.html', {'orders': orders})

    # Convert the HTML to PDF using WeasyPrint
    pdf_file = HTML(string=html_content).write_pdf()

    # Return the PDF as a response
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="order_summary.pdf"'
    return response
