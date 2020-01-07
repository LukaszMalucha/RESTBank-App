from django.urls import path, include
from rest_framework.routers import DefaultRouter

from portfolio import views

app_name = "portfolio"

router = DefaultRouter()
router.register("instruments", views.InstrumentViewSet, basename="instruments")
router.register("cash-balance", views.CashBalanceViewSet, basename="cash-balance")
router.register("asset-manager", views.AssetManagerViewSet, basename="asset-manager")
router.register("buy", views.BuyAssetViewSet, basename="buy")
router.register("sell", views.SellAssetViewSet, basename="sell")

urlpatterns = [
    path("", include(router.urls)),
]
