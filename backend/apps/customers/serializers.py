from rest_framework import serializers

from apps.customers.models import Customer, ServiceRequest


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"


class ServiceRequestSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(
        source="customer",
        queryset=Customer.objects.all(),
        write_only=True,
    )

    class Meta:
        model = ServiceRequest
        fields = "__all__"
