import pandas as pd
import backtrader as bt
import requests
import os
from datetime import datetime, timedelta, timezone

__ALL__ = ['MyLiveFeed']

class MyLiveFeed(bt.feeds.DataBase):
    params = (
        ('url', f"{os.environ.get('FINTECHFF_FEED_BASE_URL', 'http://192.168.25.127:1680')}/symbol/info/list"),
        ('historical', False),  # 是否使用历史数据
        ('fromdate', None),     # 数据的起始日期
        ('todate', None),       # 数据的结束日期
        ('symbol', None),
        ('timeframe', bt.TimeFrame.Minutes),
        ('compression', 1)
    )

    def __init__(self):
        self._timeframe = self.p.timeframe
        self._compression = self.p.compression
        super(MyLiveFeed, self).__init__()
        self.cache = {}

    def islive(self):
        return True

    def start(self):
        super(MyLiveFeed, self).start()

    def stop(self):
        super(MyLiveFeed, self).stop()

    def _load(self):
        now = datetime.now()
        start_time = (now - timedelta(minutes=1)).replace(second=0, microsecond=0)
        end_time = now.replace(second=0, microsecond=0)
        start_time_str = start_time.strftime('%Y-%m-%d %H:%M:%S')
        end_time_str = end_time.strftime('%Y-%m-%d %H:%M:%S')

        # default values for OHLC
        self.lines.datetime[0] = bt.date2num(datetime.fromtimestamp(end_time.timestamp(), timezone.utc))
        self.lines.open[0] = -1.0
        self.lines.high[0] = -1.0
        self.lines.low[0] = -1.0
        self.lines.close[0] = -1.0
        self.lines.volume[0] = -1.0

        key = f"{self.p.symbol}_{start_time_str}_{end_time_str}"
        if key not in self.cache:
            params = {
                'startTime': start_time_str,
                'endTime': end_time_str,
                'symbol': self.p.symbol
            }

            response = requests.post(self.p.url, params=params).json()
            if response.get('code') != '200':
                raise ValueError(f"API request failed: {response}")

            results = response.get('results', [])
            if len(results) > 0:
                self.cache[key] =response['results'][0]
    
        bar = self.cache.get(key, None)
        if bar is not None:
            self.lines.datetime[0] = bt.date2num(datetime.fromtimestamp(bar['timeClose'] / 1000.0, timezone.utc))
            self.lines.open[0] = bar['open']
            self.lines.high[0] = bar['high']
            self.lines.low[0] = bar['low']
            self.lines.close[0] = bar['close']
            self.lines.volume[0] = bar['vol']
        
        return True