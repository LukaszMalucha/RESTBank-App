from rest_framework.response import Response
from rest_framework import generics, viewsets, views, mixins, status, authentication, permissions
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.settings import api_settings

from core.permissions import IsAdminOrReadOnly
from core.models import Instrument, Asset, BuyTransaction, SellTransaction

from portfolio import serializers


class BaseRestrictedViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Basic authentication and permission"""
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)


class InstrumentViewSet(viewsets.ModelViewSet):
    """Create instruments in the database"""
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, IsAdminOrReadOnly)
    serializer_class = serializers.InstrumentSerializer
    queryset = Instrument.objects.all()
    queryset = queryset.exclude(name="USD")  # Exclude USD to USD transactions
    lookup_field = "slug"

    def get_queryset(self):
        """Display all instruments"""
        queryset = self.queryset
        return queryset.order_by('-name')

    def perform_create(self, serializer):
        """Create a new financial instrument"""
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AssetManagerViewSet(viewsets.ViewSet):
    """Customer's asset view"""
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.AssetSerializer
    queryset = Asset.objects.all()

    def list(self, request):
        queryset = Asset.objects.filter(owner=self.request.user).order_by('instrument')
        serializer = serializers.AssetSerializer(queryset, many=True)
        return Response(serializer.data)


class CashBalanceViewSet(BaseRestrictedViewSet):
    """Cash balance view with top-up functionality"""
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.AssetSerializer
    queryset = Asset.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        return queryset.filter(owner=self.request.user).filter(instrument__name="USD").order_by('instrument')

    def post(self, request):
        cash_serializer = serializers.AssetSerializer(data=request.data)
        cash_balance = Asset.objects.get(instrument__name="USD", owner=request.user)
        if cash_serializer.is_valid():
            top_up = int(request.data['quantity'])
            if top_up > 100000:
                raise ValidationError('Maximum amount per top up is 100k USD')
            cash_balance.quantity += top_up
            cash_balance.save()
            return Response(f"You've successfully transferred {top_up} $ to your Account."
                            f" Your current cash balance is {cash_balance.quantity}$.")

        return Response(cash_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BuyAssetViewSet(BaseRestrictedViewSet, mixins.CreateModelMixin):
    """Buy asset transaction view"""
    serializer_class = serializers.BuyTransactionSerializer
    queryset = BuyTransaction.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        return queryset.filter(owner=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        """Create a new financial instrument"""
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SellAssetViewSet(BaseRestrictedViewSet, mixins.CreateModelMixin):
    """Sell asset transaction view"""
    serializer_class = serializers.SellTransactionSerializer
    queryset = SellTransaction.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        return queryset.filter(owner=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        """Sell financial instrument"""
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
