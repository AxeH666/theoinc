from rest_framework.routers import DefaultRouter

from apps.quotations.views import QuotationItemViewSet, QuotationViewSet

app_name = "quotations"

router = DefaultRouter()
router.register(r"", QuotationViewSet, basename="quotation")
router.register(r"items", QuotationItemViewSet, basename="quotation-item")

urlpatterns = router.urls
