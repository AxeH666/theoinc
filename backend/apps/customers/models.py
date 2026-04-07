from django.db import models


class CustomerType(models.TextChoices):
    RESIDENTIAL = "residential", "Residential"
    COMMERCIAL = "commercial", "Commercial"


class ServiceRequestStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    IN_PROGRESS = "in_progress", "In Progress"
    COMPLETED = "completed", "Completed"


class Customer(models.Model):
    """Customer record for residential and commercial clients."""

    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.TextField()
    customer_type = models.CharField(
        max_length=20,
        choices=CustomerType.choices,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at", "name"]

    def __str__(self):
        return f"{self.name} ({self.get_customer_type_display()})"


class ServiceRequest(models.Model):
    """Service request raised by a customer."""

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="service_requests",
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=ServiceRequestStatus.choices,
        default=ServiceRequestStatus.PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at", "title"]

    def __str__(self):
        return f"{self.title} - {self.customer.name}"
