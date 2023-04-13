# -*- coding: utf-8 -*-
import asyncio
import openpyxl as op

import okex.Market_api as Market
from get_balance import timestamp_datetime
from websocket_example import subscribe_without_login, subscribe

flag = '1'  # 模拟盘

api_key = "2b5d8a7f-90aa-401c-af5a-9074ee40c7ca"
secret_key = "FD585FF21ED31853419E3960C840C278"
passphrase = "Casia123456!"


url = "wss://wspap.okx.com:8443/ws/v5/public?brokerId=9999"

'''
公共频道
:param channel: 频道名
:param instType: 产品类型
:param instId: 产品ID
:param uly: 合约标的指数
'''

# K线频道
channels = [{"channel": "candle1D", "instId": "BTC-USDT"}]


if __name__ == '__main__':
    marketAPI = Market.MarketAPI(api_key, secret_key, passphrase, False, flag)
    result = marketAPI.get_history_candlesticks(instId='BTC-USDT', limit='1000')
    wb = op.load_workbook("test.xlsx")
    ws = wb['Sheet1']
    print(len(result['data']))
    for re in result['data']:
        ws.insert_rows(0)
        ws['A1'] = str(timestamp_datetime(int(re[0])))
        ws['B1'] = float(re[1])
        ws['C1'] = float(re[2])
        ws['D1'] = float(re[3])
        ws['E1'] = float(re[4])
        ws['F1'] = float(re[5])
        ws['G1'] = float(re[6])

    wb.save("test.xlsx")

    # loop = asyncio.get_event_loop()
    
    # loop.run_until_complete(subscribe_without_login(url, channels))

    # loop.close()




