# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 18:06:07 2023

@author: weixh
"""

import pandas as pd
import matplotlib.pyplot as plt

# 读取数据
data = pd.read_csv('C:/weixh/HFData/SH000300.csv')
data = data[['trade_dt', 'Open', 'High', 'Low', 'Close']]
data.columns = ['date', 'open', 'high', 'low', 'price']
data['date'] = pd.to_datetime(data['date'])

# 定义变量
capital = 1_000_000  # 初始资金
position = 0  # 持仓数量
entry_price = 0  # 开仓价格
stop_loss = 0  # 止损价格
holding_period = 0  # 持仓天数
trailing_high = 0  # 持仓期内的最高价
trailing_low = 0  # 持仓期内的最低价

# 定义参数
entry_multiplier = 1.01  # 入场倍数
exit_multiplier = 0.99  # 离场倍数
max_holding_period = 20  # 最长持仓天数
stop_loss_multiplier = 0.98  # 止损倍数
stop_loss_period = 5  # 止损触发期
trailing_stop_multiplier = 0.98  # 移动止损倍数
trailing_stop_period = 5  # 移动止损触发期

# 初始化资金曲线
equity_curve = [capital]

# 定义函数
def enter_position(price):
    """
    开仓函数
    """
    global capital, position, entry_price, stop_loss, holding_period, trailing_high, trailing_low
    position = capital // price  # 全仓买入
    entry_price = price
    stop_loss = price * stop_loss_multiplier
    holding_period = 0
    trailing_high = price
    trailing_low = price
    capital -= position * price


def exit_position(price):
    """
    平仓函数
    """
    global capital, position, entry_price, stop_loss, holding_period, trailing_high, trailing_low
    capital += position * price
    position = 0
    entry_price = 0
    stop_loss = 0
    holding_period = 0
    trailing_high = 0
    trailing_low = 0


# 计算布林线
data['MA20'] = data['price'].rolling(window=20).mean()
data['std'] = data['price'].rolling(window=20).std()
data['upper'] = data['MA20'] + 2 * data['std']
data['lower'] = data['MA20'] - 2 * data['std']

# 计算动量指标
data['return'] = data['price'].pct_change()
data['momentum'] = data['return'].rolling(window=12).sum()

# 初始化信号
data['signal'] = 0

# 计算信号
for i in range(1, len(data)):
    # 布林线信号
    if data['price'][i] > data['upper'][i-1]:
        data['signal'][i] = 1
    elif data['price'][i] < data['lower'][i-1]:
        data['signal'][i] = -1
    # if (data['momentum'][i] > 0) & (data['momentum'][i-1] < 0):
    #     data['signal'][i] = 1
    # elif (data['momentum'][i] < 0) & (data['momentum'][i-1] > 0):
    #     data['signal'][i] = -1
    
    # 入场信号
    if (data['signal'][i] == 1) & (position == 0) & (holding_period == 0):
        enter_position(data['price'][i] * entry_multiplier)
    
    # 离场信号
    elif ((data['signal'][i] == -1) | (holding_period >= max_holding_period)) & (position != 0):
        exit_position(data['price'][i] * exit_multiplier)
    
    # 止损信号
    elif (data['price'][i] < stop_loss) & (position != 0):
        exit_position(stop_loss)
    
    # 移动止损信号
    elif (data['price'][i] > trailing_high) & (position != 0):
        trailing_high = data['price'][i]
        trailing_low = data['price'][i] * trailing_stop_multiplier
        stop_loss = trailing_low
    
    elif (data['price'][i] < trailing_low) & (position != 0):
        trailing_low = data['price'][i]
        trailing_high = data['price'][i] * trailing_stop_multiplier
        stop_loss = trailing_high
    
    # 更新持仓期
    if position != 0:
        holding_period += 1
    
    # 更新资金曲线
    equity_curve.append(capital + position * data['price'][i])
    
    
plt.plot( equity_curve)
plt.title('Equity Curve')
plt.xlabel('Date')
plt.ylabel('Equity')
plt.show()