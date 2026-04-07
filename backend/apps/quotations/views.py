from io import BytesIO

from django.http import FileResponse
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.quotations.models import Quotation, QuotationItem
from apps.quotations.pdf import generate_quotation_pdf
from apps.quotations.serializers import QuotationItemSerializer, QuotationSerializer


class QuotationViewSet(ModelViewSet):
    serializer_class = QuotationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Quotation.objects.select_related("customer").prefetch_related("items")

    @action(detail=True, methods=["post"])
    def calculate_total(self, request, pk=None):
        quotation = self.get_object()
        total = quotation.calculate_total()
        serializer = self.get_serializer(quotation)
        return Response({"total_amount": total, "quotation": serializer.data})

    @action(detail=True, methods=["get"], url_path="pdf")
    def pdf(self, request, pk=None):
        quotation = self.get_object()
        pdf_bytes = generate_quotation_pdf(quotation.id)
        filename = f"incetekh_quote_{quotation.id}.pdf"
        return FileResponse(
            BytesIO(pdf_bytes),
            content_type="application/pdf",
            as_attachment=True,
            filename=filename,
        )


class QuotationItemViewSet(ModelViewSet):
    queryset = QuotationItem.objects.select_related("quotation", "component").all()
    serializer_class = QuotationItemSerializer
    permission_classes = [IsAuthenticated]
