from django.db import models


class CustomerQueryIntent(models.TextChoices):
    QUOTATION_REQUEST = "quotation_request", "Quotation Request"
    SERVICE_REQUEST = "service_request", "Service Request"
    PRODUCT_INQUIRY = "product_inquiry", "Product Inquiry"
    GENERAL = "general", "General"


class KnowledgeBaseCategory(models.TextChoices):
    SOLAR_PANEL = "solar_panel", "Solar Panel"
    INVERTER = "inverter", "Inverter"
    BATTERY = "battery", "Battery"
    PRICING = "pricing", "Pricing"
    GENERAL = "general", "General"


class CustomerQuery(models.Model):
    """Stored customer conversations and AI responses."""

    customer = models.ForeignKey(
        "customers.Customer",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="queries",
    )
    query_text = models.TextField()
    intent = models.CharField(
        max_length=30,
        choices=CustomerQueryIntent.choices,
    )
    response_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        customer_name = self.customer.name if self.customer else "Anonymous"
        return f"{customer_name} - {self.get_intent_display()}"


class KnowledgeBase(models.Model):
    """Knowledge entries used by the AI assistant."""

    title = models.CharField(max_length=255)
    content = models.TextField()
    category = models.CharField(
        max_length=20,
        choices=KnowledgeBaseCategory.choices,
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "title"]

    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"
