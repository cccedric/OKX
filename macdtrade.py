import pandas as pd
import numpy as np
import talib

MACD_Strategy = {0: 'Buy', 
                 1: 'Sell', 
                 2: 'No Operation'}

#输入的close是一个长度大于slowp的list，返回值是1表示买入，2表示卖出，3表示不操作
def macdtrade(close, fastp=12, slowp=26, signalp=11):
    if len(close) < slowp:
        print('insufficient data')
        return False
    if not isinstance(close, list):
        print('input is not a list')
        return False
        
    # 计算 MACD
    datalen=len(close)
    data = np.transpose(close)
    data = pd.DataFrame(data, columns=['close'], dtype=np.double)
    data['MACD'], data['Signal'], _ = talib.MACD(data['close'].values, fastp, slowp, signalp)

    # 计算择时信号
    if data['MACD'][datalen-1] > data['Signal'][datalen-1] and data['MACD'][datalen-2] < data['Signal'][datalen-2]:
        data['Signal_Cross'][datalen] = 1
        return 0
    elif data['MACD'][datalen-1] < data['Signal'][datalen-1] and data['MACD'][datalen-2] > data['Signal'][datalen-2]:
        data['Signal_Cross'][datalen] = -1
        return 1
    else:
        return 2

