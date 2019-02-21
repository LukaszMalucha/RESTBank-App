from django.urls import path, include
from rest_framework.routers import DefaultRouter

from portfolio import views

router = DefaultRouter()
router.register('instruments', views.InstrumentViewSet)
router.register('cash_balance', views.CashBalanceViewSet)
router.register('my_portfolio', views.PortfolioViewSet, basename='my_portfolio')
router.register('buy_assets', views.BuyAssetViewSet)
router.register('sell_assets', views.SellAssetViewSet, basename='sell_assets')

app_name = 'portfolio'

urlpatterns = [
    path('', include(router.urls)),

]


