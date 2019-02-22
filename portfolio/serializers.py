from rest_framework import serializers

from core.models import Instrument, Asset, BuyTransaction, SellTransaction


class InstrumentSerializer(serializers.ModelSerializer):
    """Serializer for financial instruments"""

    class Meta:
        model = Instrument
        fields = ('id', 'name', 'symbol', 'category', 'price')
        # make id read-only
        read_only_fields = ('id',)  # Tuple!


class AssetSerializer(serializers.ModelSerializer):
    """Serializer for assets"""
    symbol = serializers.ReadOnlyField(source="instrument.symbol")

    class Meta:
        model = Asset
        fields = ('id', 'symbol', 'quantity', 'value')
        read_only_fields = '__all__',


class BuyTransactionSerializer(serializers.ModelSerializer):
    """Serializer for buy transactions"""
    symbol = serializers.ReadOnlyField(source="instrument.symbol")

    class Meta:
        model = BuyTransaction
        fields = ('id', 'symbol', 'instrument', 'quantity', 'created_at', 'value')


class SellTransactionSerializer(serializers.ModelSerializer):
    """Serializer for sell transactions"""
    symbol = serializers.ReadOnlyField(source="instrument.symbol")

    class Meta:
        model = SellTransaction
        fields = ('id', 'symbol', 'instrument', 'quantity', 'created_at', 'value')
