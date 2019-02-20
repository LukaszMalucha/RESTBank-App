from rest_framework import serializers

from core.models import User, Instrument
from django.conf import settings
from user.serializers import UserSerializer


class InstrumentSerializer(serializers.ModelSerializer):
    """Serializer for financial instruments"""

    class Meta:
        model = Instrument
        fields = ('id', 'name', 'symbol', 'price')
        # make id read-only
        read_only_fields = ('id',)  # Tuple!


# class AssetSerializer(serializers.ModelSerializer):
#     """Serializer for assets"""
#
#     class Meta:
#         model = Asset
#         fields = '__all__'
#         read_only_fields = '__all__'
#
#
# class TransactionSerializer(serializers.ModelSerializer):
#     """Serializer for transactions"""
#
#     class Meta:
#         model = Transaction
#         fields = '__all__'
#         # read_only_fields = '__all__'
#
#
# class PortfolioSerializer(serializers.ModelSerializer):
#     """Serializer for customer account"""
#     owner_email = serializers.ReadOnlyField(source="owner.email")
#     # assets = AssetSerializer(read_only=True, many=True)
#
#     class Meta:
#         model = Portfolio
#         fields = ('id', 'title', 'owner_email', 'assets')
#         read_only_fields = ('id', 'owner_email', 'assets')
#


