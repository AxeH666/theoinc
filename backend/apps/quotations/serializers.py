from rest_framework import serializers

from apps.customers.models import Customer
from apps.customers.serializers import CustomerSerializer
from apps.inventory.models import SolarComponent
from apps.quotations.models import Quotation, QuotationItem


class QuotationItemSerializer(serializers.ModelSerializer):
    quotation_id = serializers.PrimaryKeyRelatedField(
        source="quotation",
        queryset=Quotation.objects.all(),
        write_only=True,
        required=False,
    )
    component_id = serializers.PrimaryKeyRelatedField(
        source="component",
        queryset=SolarComponent.objects.all(),
        write_only=True,
    )

    class Meta:
        model = QuotationItem
        fields = "__all__"


class QuotationSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(
        source="customer",
        queryset=Customer.objects.all(),
        write_only=True,
        required=False,
        allow_null=True,
    )
    items = QuotationItemSerializer(many=True, read_only=True)

    class Meta:
        model = Quotation
        fields = "__all__"
