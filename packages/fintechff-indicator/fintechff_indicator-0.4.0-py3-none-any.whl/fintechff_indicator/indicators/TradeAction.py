import backtrader as bt
import pytz
import requests
from datetime import timedelta
from datetime import datetime
import os

__ALL__ = ['TradeAction']

class TradeAction(bt.Indicator):
    (BUY, NA, SELL) = (1, 0, -1)

    lines = ('ta',)
    params = (
        ('url', f"{os.environ.get('FINTECHFF_INDICATOR_BASE_URL', 'http://192.168.25.247:8220')}/signal/list"),
        ('symbol', 'HKEX:HTI1!'),
        ('window_size', 200)
    )


    def __init__(self):
        self.addminperiod(1)
        self.cache = {}

    def next(self):
        current_time = self.data.datetime.datetime(0).replace(tzinfo=pytz.utc).astimezone()
        current_time_str = current_time.strftime('%Y-%m-%d %H:%M:%S')

        if current_time_str not in self.cache:
            params = {
                'startTime' : current_time_str,
                'endTime' : (current_time + timedelta(minutes=self.p.window_size)).strftime('%Y-%m-%d %H:%M:%S'),
                'symbol' : self.p.symbol
            }

            response = requests.get(self.p.url, params=params).json()
            if response.get('code') != '200':
                raise ValueError(f"API request failed: {response}")

            for result in response['results']:
                close_time_str = datetime.fromtimestamp(result['closeTime'] / 1000.0).astimezone().strftime('%Y-%m-%d %H:%M:%S')
                self.cache[close_time_str] = self.NA

                trade_action_time_str = datetime.fromtimestamp(result['tradeActionTs'] / 1000.0).astimezone().strftime('%Y-%m-%d %H:%M:%S')
                self.cache[trade_action_time_str] = self.NA
                if result['tradeAction'] == 'BUY':
                    self.cache[trade_action_time_str] = self.BUY
                elif result['tradeAction'] == 'SELL':
                    self.cache[trade_action_time_str] = self.SELL

        self.lines.ta[0] = self.cache.get(current_time_str, self.NA)