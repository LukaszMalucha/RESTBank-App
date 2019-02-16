from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from user import views

router = DefaultRouter()

router.register(r'users', views.UserViewSet)

app_name = 'user'

urlpatterns = [
    path('', include(router.urls)),
]