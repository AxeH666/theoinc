from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Sum


class QuotationStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    SENT = "sent", "Sent"
    ACCEPTED = "accepted", "Accepted"
    REJECTED = "rejected", "Rejected"


class Quotation(models.Model):
    """Quotation prepared for a customer."""

    customer = models.ForeignKey(
        "customers.Customer",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="quotations",
    )
    title = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20,
        choices=QuotationStatus.choices,
        default=QuotationStatus.DRAFT,
    )
    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(0)],
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at", "title"]

    def __str__(self):
        customer_name = self.customer.name if self.customer else "Walk-in Customer"
        return f"{self.title} - {customer_name}"

    def calculate_total(self):
        """Recalculate and persist the quotation total from all line items."""
        total = self.items.aggregate(total=Sum("line_total"))["total"] or Decimal("0.00")
        self.total_amount = total
        self.save(update_fields=["total_amount", "updated_at"])
        return self.total_amount


class QuotationItem(models.Model):
    """Individual line item within a quotation."""

    quotation = models.ForeignKey(
        Quotation,
        on_delete=models.CASCADE,
        related_name="items",
    )
    component = models.ForeignKey(
        "inventory.SolarComponent",
        on_delete=models.PROTECT,
        related_name="quotation_items",
    )
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    line_total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )

    class Meta:
        ordering = ["quotation", "component__name"]

    def __str__(self):
        return f"{self.quotation.title} - {self.component.name} x {self.quantity}"
