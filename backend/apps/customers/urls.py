from rest_framework.routers import DefaultRouter

from apps.customers.views import CustomerViewSet, ServiceRequestViewSet

app_name = "customers"

router = DefaultRouter()
router.register(r"", CustomerViewSet, basename="customer")
router.register(r"service-requests", ServiceRequestViewSet, basename="service-request")

urlpatterns = router.urls
