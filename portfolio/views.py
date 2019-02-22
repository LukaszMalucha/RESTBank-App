from rest_framework.response import Response
from rest_framework import viewsets, mixins, status, views
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


from core.permissions import IsAdminOrReadOnly
from core.models import Instrument, Asset, BuyTransaction, SellTransaction
from rest_framework.views import APIView
from portfolio import serializers
from django.conf import settings
from django.shortcuts import get_object_or_404


class InstrumentViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    """Manage instruments in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAdminOrReadOnly)
    serializer_class = serializers.InstrumentSerializer
    queryset = Instrument.objects.all()


    def get_queryset(self):
        queryset = self.queryset
        return queryset.order_by('-name')

    def perform_create(self, serializer):
        """Create a new financial instrument"""
        serializer.save()


class AccountViewSet(viewsets.ViewSet):
    """Asset management in db"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.AssetSerializer
    queryset = Asset.objects.all()

    def list(self, request):
        queryset = Asset.objects.filter(owner=self.request.user)
        serializer = serializers.AssetSerializer(queryset, many=True)
        return Response(serializer.data)


class CashBalanceViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Cash Balance view"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.AssetSerializer
    queryset = Asset.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        return queryset.filter(owner=self.request.user).filter(instrument=Instrument.objects.filter(name="USD").first())

    def post(self, request):
        cash_serializer = serializers.AssetSerializer(data=request.data)
        cash_balance = Asset.objects.get(instrument__name="USD", owner=request.user)
        if cash_serializer.is_valid():
            top_up = int(request.data['quantity'])
            cash_balance.quantity += top_up
            cash_balance.save()
            return Response('TOP up success ')


class BuyAssetViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    """Buy Asset view"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.BuyTransactionSerializer
    queryset = BuyTransaction.objects.all()

    def get_queryset(self):
        queryset = self.queryset

        return queryset.filter(owner=self.request.user)

    def perform_create(self, serializer):
        """Create a new financial instrument"""
        serializer.save(owner=self.request.user)


class SellAssetViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    """Buy Asset view"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.SellTransactionSerializer
    queryset = SellTransaction.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        return queryset.filter(owner=self.request.user)

    def perform_create(self, serializer):
        """Sell  financial instrument"""
        serializer.save(owner=self.request.user)
