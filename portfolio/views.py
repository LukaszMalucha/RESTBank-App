from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.permissions import IsAdminOrReadOnly
from core.models import Instrument

from portfolio import serializers






class InstrumentViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    """Manage instruments in the database"""
    queryset = Instrument.objects.all()
    serializer_class = serializers.InstrumentSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAdminOrReadOnly)

    # def get_queryset(self):
    #     queryset = self.queryset
    #     return queryset.order_by('-name')

    def perform_create(self, serializer):
        # self.permission_classes = (IsAdminOrReadOnly,)
        """Create a new financial instrument"""
        serializer.save()