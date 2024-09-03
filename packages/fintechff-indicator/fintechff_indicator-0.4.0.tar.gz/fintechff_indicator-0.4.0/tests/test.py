import backtrader as bt
import datetime
import requests
import logging
import pandas as pd
from feeds.MyData import MyData
import pytz
from indicators.TradeAction import TradeAction
from indicators.LongTermDirection import LongTermDirection
from indicators.ShortTermDirection import ShortTermDirection

# 创建一个策略类
class SmaCross(bt.Strategy):
    # 定义参数
    params = (('short_period', 10), ('long_period', 30),)

    def __init__(self):
        self.sma_short = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.short_period)
        self.sma_long = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.long_period)
        self.ta = TradeAction()
        self.ltd = LongTermDirection()
        self.std = ShortTermDirection()

    def next(self):

        # print(f"datetime: {self.data.datetime.datetime().astimezone(pytz.timezone('Asia/Shanghai'))}, open: {self.data.open[0]}, high: {self.data.high[0]}, low: {self.data.low[0]}, close: {self.data.close[0]}")
        # print(f"sma_short: {self.sma_short[0]}")

        # 移动平均线交叉策略
        if self.sma_short > self.sma_long and self.std[0] == self.std.BULLISH:  # 短期均线上穿长期均线，买入
            self.buy()
        elif self.sma_short < self.sma_long and self.std[0] == self.std.BEARISH:  # 短期均线下穿长期均线，卖出
            self.sell()


if __name__ == '__main__':
    cerebro = bt.Cerebro()

    my_data = MyData(start_time="2024-09-02 00:00:00", end_time="2024-09-02 23:59:00", symbol="HKEX:HTI1!")
    cerebro.adddata(my_data)

    # 添加策略
    cerebro.addstrategy(SmaCross)

    # 设定初始资金
    cerebro.broker.setcash(10000.0)

    # 执行回测
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('Ending Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # 绘制结果
    cerebro.plot()