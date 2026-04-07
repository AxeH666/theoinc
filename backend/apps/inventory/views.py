from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.inventory.models import SolarComponent, StockTransaction
from apps.inventory.serializers import (
    SolarComponentSerializer,
    StockTransactionSerializer,
)


class SolarComponentViewSet(ModelViewSet):
    queryset = SolarComponent.objects.all()
    serializer_class = SolarComponentSerializer
    permission_classes = [IsAuthenticated]


class StockTransactionViewSet(ModelViewSet):
    serializer_class = StockTransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = StockTransaction.objects.select_related("component").all()
        component_id = self.request.query_params.get("component")
        if component_id:
            queryset = queryset.filter(component_id=component_id)
        return queryset
