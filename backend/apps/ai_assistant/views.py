from rest_framework import mixins
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from apps.ai_assistant.models import CustomerQuery, KnowledgeBase
from apps.ai_assistant.serializers import (
    CustomerQuerySerializer,
    KnowledgeBaseSerializer,
)
from apps.ai_assistant.services import handle_customer_query


class CustomerQueryViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet,
):
    queryset = CustomerQuery.objects.select_related("customer").all()
    serializer_class = CustomerQuerySerializer
    permission_classes = [IsAuthenticated]


class KnowledgeBaseViewSet(ModelViewSet):
    queryset = KnowledgeBase.objects.all()
    serializer_class = KnowledgeBaseSerializer
    permission_classes = [IsAuthenticated]


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def chat(request):
    query_text = request.data.get("query", "").strip()
    customer_id = request.data.get("customer_id")

    if not query_text:
        return Response(
            {"detail": "The 'query' field is required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    customer_query = handle_customer_query(
        query_text=query_text,
        customer_id=customer_id,
    )
    serializer = CustomerQuerySerializer(customer_query)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
