import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import talib

# 读取数据
data = pd.read_csv('SH000300.csv')
data.rename(columns={'Close': 'close', 'trade_dt': 'date'}, inplace=True)

# 计算 MACD
data['MACD'], data['Signal'], _ = talib.MACD(data['close'].values, fastperiod=12, slowperiod=26, signalperiod=9)
print(data['MACD'])

# 计算择时信号
data['Signal_Cross'] = 0
for i in range(1, len(data)):
    if data['MACD'][i-1] > data['Signal'][i-1] and data['MACD'][i-2] < data['Signal'][i-2]:
        data['Signal_Cross'][i] = 1
        print(i,'signal 1')
    elif data['MACD'][i-1] < data['Signal'][i-1] and data['MACD'][i-2] > data['Signal'][i-2]:
        data['Signal_Cross'][i] = -1
        print(i,'signal -1')

data['Signal_Cross'][1] = 1
# 计算收益率和资金曲线
capital = 1000000.0  # 起始资金
data['Shares'] = 0.0
data['Capital'] = 0.0
for i in range(1, len(data)):
    if data['Signal_Cross'][i] == 1:
        data['Shares'][i] = capital / data['close'][i-1]
        capital = 0
    elif data['Signal_Cross'][i] == -1:
        capital = data['close'][i] * data['Shares'][i-1]
        data['Shares'][i] = 0
    else:
        data['Shares'][i] = data['Shares'][i-1]
    data['Capital'][i] = capital

data['Returns'] = np.log(data['close'] / data['close'].shift(1))
data['Cumulative_Returns'] = data['Returns'].cumsum()

print(data['Cumulative_Returns'])

plt.plot(data['Cumulative_Returns'])
plt.show()
