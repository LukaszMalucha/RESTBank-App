from rest_framework import serializers

from core.models import User, Instrument, Asset, BuyTransaction, SellTransaction
from django.conf import settings
from user.serializers import UserSerializer


class InstrumentSerializer(serializers.ModelSerializer):
    """Serializer for financial instruments"""

    class Meta:
        model = Instrument
        fields = ('id', 'name', 'symbol', 'price')
        # make id read-only
        read_only_fields = ('id',)  # Tuple!


class AssetSerializer(serializers.ModelSerializer):
    """Serializer for assets"""
    symbol = serializers.ReadOnlyField(source="instrument.symbol")

    class Meta:
        model = Asset
        fields = ('id', 'symbol', 'quantity')
        read_only_fields = '__all__',


class BuyTransactionSerializer(serializers.ModelSerializer):
    """Serializer for assets"""
    symbol = serializers.ReadOnlyField(source="instrument.symbol")

    class Meta:
        model = BuyTransaction
        fields = ('id', 'symbol', 'instrument', 'quantity', 'created_at', 'value')


class BuyTransactionSerializer(serializers.ModelSerializer):
    """Serializer for assets"""
    symbol = serializers.ReadOnlyField(source="instrument.symbol")

    class Meta:
        model = BuyTransaction
        fields = ('id', 'symbol', 'instrument', 'quantity', 'created_at', 'value')


class SellTransactionSerializer(serializers.ModelSerializer):
    """Serializer for assets"""
    symbol = serializers.ReadOnlyField(source="instrument.symbol")

    class Meta:
        model = SellTransaction
        fields = ('id', 'symbol', 'instrument', 'quantity', 'created_at', 'value')
