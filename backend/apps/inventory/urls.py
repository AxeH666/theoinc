from rest_framework.routers import DefaultRouter

from apps.inventory.views import SolarComponentViewSet, StockTransactionViewSet

app_name = "inventory"

router = DefaultRouter()
router.register(r"components", SolarComponentViewSet, basename="solar-component")
router.register(
    r"stock-transactions",
    StockTransactionViewSet,
    basename="stock-transaction",
)

urlpatterns = router.urls
