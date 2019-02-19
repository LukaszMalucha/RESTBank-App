from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from portfolio import views

router = DefaultRouter()
router.register('instruments', views.InstrumentViewSet)
router.register('cash_balance', views.CashBalanceViewSet)

app_name = 'portfolio'

urlpatterns = [
    path('', include(router.urls))
]


