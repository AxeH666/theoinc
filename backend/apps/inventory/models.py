from django.core.validators import MinValueValidator
from django.db import models


class ComponentType(models.TextChoices):
    PANEL = "panel", "Panel"
    INVERTER = "inverter", "Inverter"
    BATTERY = "battery", "Battery"
    CABLE = "cable", "Cable"
    MOUNTING = "mounting", "Mounting"
    OTHER = "other", "Other"


class StockTransactionType(models.TextChoices):
    PURCHASE = "purchase", "Purchase"
    SALE = "sale", "Sale"
    ADJUSTMENT = "adjustment", "Adjustment"


class SolarComponent(models.Model):
    """Inventory item used in solar energy projects."""

    name = models.CharField(max_length=255)
    component_type = models.CharField(
        max_length=20,
        choices=ComponentType.choices,
    )
    brand = models.CharField(max_length=255)
    unit_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    stock_quantity = models.IntegerField(validators=[MinValueValidator(0)])
    minimum_stock_level = models.IntegerField(
        default=5,
        validators=[MinValueValidator(0)],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name", "-created_at"]

    def __str__(self):
        return f"{self.name} ({self.brand})"


class StockTransaction(models.Model):
    """Stock movement record for a solar component."""

    component = models.ForeignKey(
        SolarComponent,
        on_delete=models.CASCADE,
        related_name="stock_transactions",
    )
    transaction_type = models.CharField(
        max_length=20,
        choices=StockTransactionType.choices,
    )
    quantity = models.IntegerField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "component__name"]

    def __str__(self):
        return (
            f"{self.get_transaction_type_display()} - "
            f"{self.component.name} ({self.quantity})"
        )
