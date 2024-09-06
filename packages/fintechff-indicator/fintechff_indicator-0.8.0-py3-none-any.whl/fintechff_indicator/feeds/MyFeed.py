import pandas as pd
import backtrader as bt
import requests
import os

__ALL__ = ['MyFeed']

class MyFeed(bt.feeds.PandasData):
    params = (
        ('volume', 'vol'),
        ('openinterest', None),
        ('url', f"{os.environ.get('FINTECHFF_FEED_BASE_URL', 'http://192.168.25.127:1680')}/symbol/info/list"),
        ('params', None),
        ('start_time', None),
        ('end_time', None),
        ('symbol', None),
        ('timeframe', bt.TimeFrame.Minutes),
        ('compression', 1)
    )

    def __init__(self):
        self._timeframe = self.p.timeframe
        self._compression = self.p.compression
        self.fetch_and_process_data()
        super(MyFeed, self).__init__()

    def fetch_and_process_data(self):
        if self.p.url is None or self.p.start_time is None or self.p.end_time is None or self.p.symbol is None:
            raise ValueError("Missing required parameters")

        params = {
            'startTime': self.p.start_time,
            'endTime': self.p.end_time,
            'symbol': self.p.symbol
        }

        response = requests.post(self.p.url, params=params).json()
        if response.get('code') != '200':
            raise ValueError(f"API request failed: {response}")

        df = pd.DataFrame(response['results'])

        df.sort_values(by=['timeClose', 'updateTime'], ascending=[True, False], inplace=True)
        df = df.drop_duplicates(subset=['timeClose'], keep='first')

        df['timeClose'] = pd.to_datetime(df['timeClose'], unit='ms').dt.tz_localize('UTC').dt.tz_convert(None)
        df.set_index('timeClose', inplace=True)
        df.sort_index(inplace=True)

        self.p.dataname = df