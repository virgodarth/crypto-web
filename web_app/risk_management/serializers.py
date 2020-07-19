import ccxt
from django.utils import timezone
from rest_framework import serializers
from rest_framework.fields import empty

from web_app.settings import settings


class RiskChartSerializer(serializers.Serializer):
    ticker = serializers.CharField()
    currency = serializers.CharField()
    symbol = serializers.SerializerMethodField()
    timeframe = serializers.CharField()
    from_datetime = serializers.CharField()
    ohlcv = serializers.JSONField()
    sma = serializers.JSONField()
    stda = serializers.JSONField()
    
    def __init__(self, instance=None, data=empty, **kwargs):
        super().__init__(instance=instance, data=data, **kwargs)
        params = {
            'apiKey': settings.BIBOX['API_KEY'], 'secret': settings.BIBOX['SECRET_KEY'],
            'timeout': 30000,
            'enableRateLimit': True
        }
        self.ex = ccxt.bibox(params)
      
    def get_symbol(self, obj):
        return f"{obj['ticker']}/{obj['currency']}"
    
    # def to_representation(self, instance):
    #     return super().to_representation(instance)
