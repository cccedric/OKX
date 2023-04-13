# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 19:34:03 2023

@author: weixh
"""

import pandas as pd
import talib
import matplotlib.pyplot as plt

# 读取数据
data = pd.read_csv('/weixh/HFData/SH000300.csv')
data = data[['trade_dt', 'Open', 'High', 'Low', 'Close']]
data.columns = ['date', 'open', 'high', 'low', 'price']
data['date'] = pd.to_datetime(data['date'])

# 计算TRIX指标
data['trix'] = talib.TRIX(data['price'], timeperiod=30)
data['signal'] = data['trix'].diff()

# 初始化资金曲线
capital = 1_000_000
equity_curve = [capital]

# 定义参数
buy_threshold = 0.002
sell_threshold = -0.002

# 定义变量
position = 0
entry_price = 0

# 定义函数
def enter_position(price):
    """
    开仓函数
    """
    global capital, position, entry_price
    position = capital // price  # 全仓买入
    entry_price = price
    capital -= position * price

def exit_position(price):
    """
    平仓函数
    """
    global capital, position, entry_price
    capital += position * price
    position = 0
    entry_price = 0

# 计算信号
for i in range(1, len(data)):
    if data['signal'][i] > buy_threshold and position == 0:
        # 金叉买入
        enter_position(data['price'][i])
    elif data['signal'][i] < sell_threshold and position != 0:
        # 死叉卖出
        exit_position(data['price'][i])
    equity_curve.append(capital + position * data['price'][i])

# 绘制资金曲线
plt.plot(data['date'], equity_curve)
plt.title('TRIX Timing Strategy')
plt.xlabel('Date')
plt.ylabel('Equity Curve ($)')
plt.show()
