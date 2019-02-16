from rest_framework import generics, authentication, permissions, viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import renderer_classes
from rest_framework.settings import api_settings
from user.serializers import UserSerializer, AuthTokenSerializer
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from core.models import User
from django.shortcuts import get_object_or_404




class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer  # generic view - specify serializer you want to use only
    renderer_classes = (TemplateHTMLRenderer,)

    def list(self, request, *args, **kwargs):
        return Response({'data': self.queryset}, template_name='profile_list.html')

    def retrieve(self, request, pk):
        profile = get_object_or_404(User, id=pk)
        return Response({'data': profile}, template_name='user_detail.html')