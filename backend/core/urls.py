from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("demo/", TemplateView.as_view(template_name="demo.html")),
    path("api/health/", include("health.urls")),
    # API v1 (per docs/04_API_CONTRACT.md base path: /api/v1)
    path("api/v1/auth/", include("apps.auth.urls")),
    path("api/v1/users/", include("apps.users.urls")),
    path("api/v1/audit/", include("apps.audit.urls")),
    path("api/v1/customers/", include("apps.customers.urls")),
    path("api/v1/inventory/", include("apps.inventory.urls")),
    path("api/v1/quotations/", include("apps.quotations.urls")),
    path("api/v1/ai-assistant/", include("apps.ai_assistant.urls")),
    path("api/v1/ledger/", include("apps.ledger.urls")),
    # Payments endpoints are defined directly under /api/v1 (e.g., /api/v1/batches)
    path("api/v1/", include("apps.payments.urls")),
]
