from rest_framework import serializers

from core.models import Instrument, Portfolio, CashBalance, Transaction, User
from django.conf import settings
from user.serializers import UserSerializer


class InstrumentSerializer(serializers.ModelSerializer):
    """Serializer for financial instruments"""

    class Meta:
        model = Instrument
        fields = ('id', 'name', 'symbol', 'price')
        # make id read-only
        read_only_fields = ('id',)  # Tuple!


class PortfolioSerializer(serializers.ModelSerializer):
    """Serializer for customer account"""

    class Meta:
        model = Portfolio
        fields = {'id', 'title', 'owner', 'instruments', 'cash'}
        read_only_fields = '__all__'


class CashBalanceSerializer(serializers.ModelSerializer):
    """Serializer for customer's cash balance"""
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    email = serializers.ReadOnlyField(source="owner.email")

    class Meta:
        model = CashBalance
        fields = ('id','owner', 'email', 'cash_balance')
        read_only_fields = ('id','owner')


class TransactionSerializer(serializers.ModelSerializer):
    """Serializer for transactions"""

    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = '__all__'
