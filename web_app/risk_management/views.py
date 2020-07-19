import json

import ccxt
import pandas as pd

from rest_framework import generics, views
from rest_framework.response import Response

from risk_management.renderers import RiskChartAPIRenderer
from risk_management.serializers import RiskChartSerializer
from web_app.settings import settings


class RiskChartView(views.APIView):
    serializer_class = RiskChartSerializer
    renderer_classes = (RiskChartAPIRenderer, )
    template_name = 'risk_management/risk_chart.html'
    
    def get(self, request, ticker, *args, **kwargs):
        ticker = ticker.upper()
        currency = 'USDT'
        symbol = f'{ticker}/{currency}'
        timeframe = '1d'
        from_datetime = '2015-01-01 00:00:00'
        params = {
            'apiKey': settings.BIBOX['API_KEY'], 'secret': settings.BIBOX['SECRET_KEY'],
            'timeout': 30000,
            'enableRateLimit': True
        }
        ccxt_ex = ccxt.bibox(params)
        from_timestamp = ccxt_ex.parse8601(from_datetime)
        ohlcv = ccxt_ex.fetch_ohlcv(symbol, timeframe, from_timestamp)
        
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        # print(list(df['close'].rolling(20).std().fillna('null')))
        sma = [
            list(df['close'].rolling(20).mean().fillna(0)),
            list(df['close'].rolling(50).mean().fillna(0)),
            list(df['close'].rolling(100).mean().fillna(0)),
        ]
        stda = [
            list(df['close'].rolling(20).std().fillna(0)),
            list(df['close'].rolling(50).std().fillna(0)),
            list(df['close'].rolling(100).std().fillna(0)),
        ]
        
        # print(type(df['close'].rolling(20).std().values), df['close'].rolling(20).std().values)
        serializer = self.serializer_class(data={
            'ticker': ticker, 'currency': currency,
            'timeframe': '1d', 'from_datetime': '2017-01-01 00:00:00',
            'ohlcv': ohlcv,
            'sma': sma, 'stda': stda,
        })
        serializer.is_valid()
        return Response(serializer.data)
