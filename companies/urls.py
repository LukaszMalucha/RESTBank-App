from django.urls import path

from companies import views

app_name = 'user'

urlpatterns = [
    path('', views.company_view, name='companies'),
]
