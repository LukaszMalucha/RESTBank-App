from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.permissions import IsAdminOrReadOnly
from core.models import Instrument, Asset, BuyTransaction, SellTransaction

from portfolio import serializers


class BaseRestrictedVIewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Basic authentication and permission"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


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


class CashBalanceViewSet(BaseRestrictedVIewSet):
    """Cash Balance view"""
    serializer_class = serializers.AssetSerializer
    queryset = Asset.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        return queryset.filter(owner=self.request.user).filter(instrument__name="USD")

    def post(self, request):
        cash_serializer = serializers.AssetSerializer(data=request.data)
        cash_balance = Asset.objects.get(instrument__name="USD", owner=request.user)
        if cash_serializer.is_valid():
            top_up = int(request.data['quantity'])
            cash_balance.quantity += top_up
            cash_balance.save()
            return Response(f"You've successfully transferred {top_up} $ to your Account."
                            f" Your current cash balance is {cash_balance.quantity}$.")
        return Response(cash_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InstrumentViewSet(BaseRestrictedVIewSet, mixins.CreateModelMixin):
    """Manage instruments in the database"""
    permission_classes = (IsAuthenticated, IsAdminOrReadOnly)
    serializer_class = serializers.InstrumentSerializer
    queryset = Instrument.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        return queryset.order_by('-name')

    def perform_create(self, serializer):
        """Create a new financial instrument"""
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BuyAssetViewSet(BaseRestrictedVIewSet, mixins.CreateModelMixin):
    """Buy Asset view"""
    serializer_class = serializers.BuyTransactionSerializer
    queryset = BuyTransaction.objects.all()

    def get_queryset(self):
        queryset = self.queryset

        return queryset.filter(owner=self.request.user)

    def perform_create(self, serializer):
        """Create a new financial instrument"""
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SellAssetViewSet(BaseRestrictedVIewSet, mixins.CreateModelMixin):
    """Buy Asset view"""
    serializer_class = serializers.SellTransactionSerializer
    queryset = SellTransaction.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        return queryset.filter(owner=self.request.user)

    def perform_create(self, serializer):
        """Sell  financial instrument"""
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
