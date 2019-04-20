from django.urls import path, include
from rest_framework.routers import DefaultRouter

from portfolio import views

router = DefaultRouter()
router.register('instruments', views.InstrumentViewSet)
router.register('cash_balance', views.CashBalanceViewSet)
router.register('account', views.AccountViewSet, basename='account')
router.register('buy', views.BuyAssetViewSet)
router.register('sell', views.SellAssetViewSet, basename='sell')

app_name = 'portfolio'

urlpatterns = [
    path('', include(router.urls)),

]


