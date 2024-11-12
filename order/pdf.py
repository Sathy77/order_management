
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from django.http import HttpResponse
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from order import models as MODELS_ORDE
from rest_framework.decorators import api_view

# Register Bangla font
pdfmetrics.registerFont(TTFont('BanglaFont', 'pdf/bangla/kalpurush.ttf'))

@api_view(['GET'])
def generate_ordersummary_pdf(request):
    # Set up response and PDF canvas
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="ordersummary.pdf"'
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    y_position = height - 80

    # Column settings
    col_positions = [50, 120, 190, 250, 350, 420, 540]
    col_titles = ["Invoice No", "Customer", "Date", "Payment Mode", "Grand Total", "Delivery Zone", "Status"]
    line_height = 20

    # Title
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, y_position, "Order Summary List")
    y_position -= 40

    # Column Headers
    p.setFont("Helvetica-Bold", 10)
    for idx, title in enumerate(col_titles):
        p.drawString(col_positions[idx], y_position, title)
    y_position -= line_height

    # Content Rows
    orders = MODELS_ORDE.Ordersummary.objects.all()
    for order in orders:
        if y_position < 50:
            p.showPage()
            y_position = height - 80
            for idx, title in enumerate(col_titles):
                p.drawString(col_positions[idx], y_position, title)
            y_position -= line_height

        # Data for each column
        data = [
            order.invoice_no or "N/A",
            order.user.name or "N/A",
            str(order.date) or "N/A",
            order.payment_mode or "N/A",
            f"${order.grand_total:.2f}",
        ]

        # Draw each column data except the Bangla field
        p.setFont("Helvetica", 9)
        for idx, text in enumerate(data):
            p.drawString(col_positions[idx], y_position, text)

        # Draw the Delivery Zone name in Bangla font
        p.setFont("BanglaFont", 9)
        delivery_zone_name = order.deliveryzone.name if order.deliveryzone else "N/A"
        p.drawString(col_positions[5], y_position, delivery_zone_name)

        p.setFont("Helvetica", 9)
        status = order.order_status if order.order_status else "N/A"
        p.drawString(col_positions[6], y_position, status)

        # Reset for next row
        y_position -= line_height

    # Finalize PDF
    p.showPage()
    p.save()
    return response