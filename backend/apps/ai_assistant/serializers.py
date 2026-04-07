from rest_framework import serializers

from apps.ai_assistant.models import CustomerQuery, KnowledgeBase
from apps.customers.models import Customer
from apps.customers.serializers import CustomerSerializer


class CustomerQuerySerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(
        source="customer",
        queryset=Customer.objects.all(),
        write_only=True,
        required=False,
        allow_null=True,
    )

    class Meta:
        model = CustomerQuery
        fields = "__all__"


class KnowledgeBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = KnowledgeBase
        fields = "__all__"
