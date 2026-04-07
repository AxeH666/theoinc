from rest_framework import serializers

from apps.inventory.models import SolarComponent, StockTransaction


class SolarComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolarComponent
        fields = "__all__"


class StockTransactionSerializer(serializers.ModelSerializer):
    component = SolarComponentSerializer(read_only=True)
    component_id = serializers.PrimaryKeyRelatedField(
        source="component",
        queryset=SolarComponent.objects.all(),
        write_only=True,
    )

    class Meta:
        model = StockTransaction
        fields = "__all__"
