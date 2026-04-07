from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas

from apps.quotations.models import Quotation


def _draw_right_text(pdf, text, x, y, font_name="Helvetica", font_size=10):
    width = stringWidth(text, font_name, font_size)
    pdf.setFont(font_name, font_size)
    pdf.drawString(x - width, y, text)


def generate_quotation_pdf(quotation_id):
    quotation = (
        Quotation.objects.select_related("customer")
        .prefetch_related("items", "items__component")
        .get(pk=quotation_id)
    )

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    page_width, page_height = A4

    left = 20 * mm
    right = page_width - 20 * mm
    y = page_height - 25 * mm

    pdf.setTitle(f"Quotation {quotation.id}")

    pdf.setFont("Helvetica-Bold", 20)
    pdf.setFillColor(colors.HexColor("#F97316"))
    pdf.drawString(left, y, "Incetekh Energy Solutions")

    y -= 8 * mm
    pdf.setFillColor(colors.black)
    pdf.setFont("Helvetica", 12)
    pdf.drawString(left, y, "Solar System Quotation")

    _draw_right_text(
        pdf,
        f"Date: {quotation.created_at.strftime('%Y-%m-%d')}",
        right,
        y + 4 * mm,
    )
    _draw_right_text(pdf, f"Quotation ID: {quotation.id}", right, y - 2 * mm)

    y -= 18 * mm
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(left, y, "Customer")
    y -= 6 * mm

    pdf.setFont("Helvetica", 10)
    if quotation.customer:
        pdf.drawString(left, y, quotation.customer.name)
        y -= 5 * mm
        for line in quotation.customer.address.splitlines() or [""]:
            pdf.drawString(left, y, line)
            y -= 5 * mm
    else:
        pdf.drawString(left, y, "Walk-in Customer")
        y -= 5 * mm

    y -= 6 * mm
    row_height = 9 * mm
    table_width = right - left
    column_widths = [78 * mm, 20 * mm, 35 * mm, table_width - (78 * mm + 20 * mm + 35 * mm)]
    headers = ["Component", "Qty", "Unit Price (Rs)", "Total (Rs)"]

    x = left
    pdf.setFillColor(colors.HexColor("#1F2937"))
    pdf.rect(left, y - row_height + 2, table_width, row_height, fill=1, stroke=0)
    pdf.setFillColor(colors.white)
    pdf.setFont("Helvetica-Bold", 10)
    for header, width in zip(headers, column_widths):
        pdf.drawString(x + 3 * mm, y - 5 * mm, header)
        x += width

    y -= row_height
    pdf.setFillColor(colors.black)
    pdf.setFont("Helvetica", 10)

    items = quotation.items.all()
    for item in items:
        x = left
        pdf.setStrokeColor(colors.HexColor("#D1D5DB"))
        pdf.rect(left, y - row_height + 2, table_width, row_height, fill=0, stroke=1)

        values = [
            item.component.name,
            str(item.quantity),
            f"{item.unit_price:.2f}",
            f"{item.line_total:.2f}",
        ]
        for index, (value, width) in enumerate(zip(values, column_widths)):
            if index == 0:
                pdf.drawString(x + 3 * mm, y - 5 * mm, value)
            else:
                _draw_right_text(pdf, value, x + width - 3 * mm, y - 5 * mm)
            x += width
        y -= row_height

    pdf.setFillColor(colors.HexColor("#FFF7ED"))
    pdf.rect(left, y - row_height + 2, table_width, row_height, fill=1, stroke=1)
    pdf.setFillColor(colors.black)
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(left + 3 * mm, y - 5 * mm, "Total")
    _draw_right_text(pdf, f"{quotation.total_amount:.2f}", right - 3 * mm, y - 5 * mm, "Helvetica-Bold", 10)

    footer_text = "Valid for 30 days | incetekh@gmail.com | Udupi, Karnataka"
    pdf.setFont("Helvetica", 9)
    pdf.setFillColor(colors.HexColor("#6B7280"))
    _draw_right_text(pdf, footer_text, right, 15 * mm)

    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    return buffer.getvalue()
