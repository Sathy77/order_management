from django.views import View
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from django.utils import timezone
from order import models as MODELS_ORDE  # Replace with your actual app name
from io import BytesIO

class OrderSummaryPDFView(View):
    def get(self, request, *args, **kwargs):
        # Create a BytesIO buffer for the PDF
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        
        # Set up the PDF
        c.setFont("Helvetica-Bold", 12)
        c.drawString(200, 820, "Order Summary Report")
        c.setFont("Helvetica", 10)
        c.drawString(50, 800, f"Date: {timezone.now().strftime('%Y-%m-%d')}")
        c.line(50, 795, 550, 795)
        
        # Column Headers
        headers = ["Invoice No", "Customer", "Date", "Delivery Zone", "Payment Mode", "Total", "Status"]
        x_offsets = [50, 100, 200, 300, 380, 460, 520]
        for i, header in enumerate(headers):
            c.drawString(x_offsets[i], 770, header)
        c.line(50, 765, 550, 765)
        
        # Fetch orders
        orders = MODELS_ORDE.Ordersummary.objects.filter(invoice_no__isnull=False)
        y = 750  # Start position for rows
        
        for order in orders:
            # Get data for each order row
            deliveryzone_name = order.deliveryzone.name if order.deliveryzone else 'N/A'
            payment_mode = order.get_payment_mode_display()
            order_status = order.get_order_status_display()

            # Row data
            row_data = [
                order.invoice_no,
                order.user.name,
                order.date.strftime('%Y-%m-%d'),
                deliveryzone_name,
                payment_mode,
                f"{order.grand_total:.2f}",
                order_status
            ]
            
            # Draw each row in the PDF
            for i, data in enumerate(row_data):
                c.drawString(x_offsets[i], y, str(data))
            y -= 20
            
            # Create a new page if space runs out
            if y < 50:
                c.showPage()
                y = 770
                for i, header in enumerate(headers):
                    c.drawString(x_offsets[i], y, header)
                y -= 20
        
        c.save()
        
        # Get the PDF data from the buffer and return it as a response
        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="order_summary_report.pdf"'
        
        return response