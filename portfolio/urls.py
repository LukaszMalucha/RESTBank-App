from django.urls import path, include
from rest_framework.routers import DefaultRouter

from portfolio import views

router = DefaultRouter()
router.register('instruments', views.InstrumentViewSet)
router.register('cash_balance', views.CashBalanceViewSet)
router.register('my_portfolio', views.PortfolioViewSet, basename='my_portfolio')

app_name = 'portfolio'

urlpatterns = [
    path('', include(router.urls)),

]


