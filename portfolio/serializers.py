from rest_framework import serializers

from core.models import Instrument


class InstrumentSerializer(serializers.ModelSerializer):
    """Serializer for financial instruments"""

    class Meta:
        model = Instrument
        fields = ('id', 'name', 'symbol', 'price')
        # make id read-only
        read_only_fields = ('id',) # Tuple!