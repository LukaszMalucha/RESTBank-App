from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.permissions import IsAdminOrReadOnly
from core.models import Instrument

from portfolio import serializers
from django.conf import settings


class InstrumentViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    """Manage instruments in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAdminOrReadOnly)
    queryset = Instrument.objects.all()
    serializer_class = serializers.InstrumentSerializer

    def get_queryset(self):
        queryset = self.queryset
        return queryset.order_by('-name')

    def perform_create(self, serializer):
        """Create a new financial instrument"""
        serializer.save()







# class PortfolioViewSet(viewsets.ViewSet):
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticated,)
#     queryset = Portfolio.objects.all()
#     serializer_class = serializers.PortfolioSerializer
#
#     def list(self, request):
#         queryset = Portfolio.objects.filter(owner=self.request.user)
#         serializer = serializers.PortfolioSerializer(queryset, many=True)
#         return Response(serializer.data)
#
#
#
# class TransactionViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
#     pass
