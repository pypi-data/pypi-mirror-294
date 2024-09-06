import backtrader as bt
import os
import pytz
import requests
from datetime import datetime, timedelta

__ALL__ = ['ShortTermDirection']

class ShortTermDirection(bt.Indicator):
    (BEARISH, NA, BULLISH) = (-1, 0, 1)

    lines = ('std',)
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

                short_term_dir_time_str = datetime.fromtimestamp(result['shortTermDirTs'] / 1000.0).astimezone().strftime('%Y-%m-%d %H:%M:%S')
                self.cache[short_term_dir_time_str] = self.NA
                if result['shortTermDir'] == 'BULLISH':
                    self.cache[short_term_dir_time_str] = self.BULLISH
                elif result['shortTermDir'] == 'BEARISH':
                    self.cache[short_term_dir_time_str] = self.BEARISH

        self.lines.std[0] = self.cache.get(current_time_str, self.NA)