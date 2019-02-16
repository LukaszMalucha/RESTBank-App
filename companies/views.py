from django.http import HttpRequest
from django.shortcuts import render, render_to_response
from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer

from companies.serializers import CompanySerializer
from .models import Company


def company_view(request):
    assert isinstance(request, HttpRequest)
    queryset = Company.objects.all()
    serializer_class = CompanySerializer(queryset,many=True)
    return render( request,'companies.html',{ 'data':serializer_class.data,})