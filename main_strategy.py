# -*- coding: utf-8 -*-
import asyncio
import websockets
import json
import datetime

import okex.Market_api as Market
from macdtrade import macdtrade, MACD_Strategy

flag = '1'  # 模拟盘

api_key = "2b5d8a7f-90aa-401c-af5a-9074ee40c7ca"
secret_key = "FD585FF21ED31853419E3960C840C278"
passphrase = "Casia123456!"

url = "wss://wspap.okx.com:8443/ws/v5/public?brokerId=9999"

candlesticks_bar = "1m"
candlesticks_channel = "candle"+candlesticks_bar

inst_id = "BTC-USDT"

channels = [{"channel": candlesticks_channel, 
             "instId": inst_id}]

buffer_len = 30


def get_timestamp():
    now = datetime.datetime.now()
    t = now.isoformat("T", "milliseconds")
    return t + "Z"

def update_candlesticks_buffer(candlesticks_buffer, data):
    buffer_is_updated = False
    if int(data[8]) == 1:
        buffer_is_updated = True
        candlesticks_buffer.append(data[4])
        if len(candlesticks_buffer) > buffer_len:
            candlesticks_buffer.pop(0)
        print(get_timestamp(), " candlesticks_buffer updated")
    return candlesticks_buffer, buffer_is_updated

async def main_loop(url, channels, candlesticks_buffer):
    while True:
        try:
            async with websockets.connect(url) as ws:
                sub_param = {"op": "subscribe", "args": channels}
                sub_str = json.dumps(sub_param)
                await ws.send(sub_str)
                print(f"send: {sub_str}")

                while True:
                    try:
                        res = await asyncio.wait_for(ws.recv(), timeout=25)
                    except (asyncio.TimeoutError, websockets.exceptions.ConnectionClosed) as e:
                        print("等待信息超时")
                        try:
                            await ws.send('ping')
                            res = await ws.recv()
                            print("ping res", res)
                            continue
                        except Exception as e:
                            print("连接关闭，正在重连……")
                            break

                    res = eval(res)
                    # print(res)
                    if 'event' in res:
                        continue
                    candlesticks_buffer, buffer_is_updated = update_candlesticks_buffer(candlesticks_buffer, res['data'][0])
                    if buffer_is_updated:
                        # Calculate strategy using candlesticks buffer here
                        strategy = macdtrade(candlesticks_buffer)
                        print("MACD strategy: ", MACD_Strategy[strategy])
                        continue

        except Exception as e:
            print("[Error]", e)
            print("连接断开，正在重连……")
            continue

if __name__ == '__main__':
    candlesticks_buffer = list()

    # Read the last candlesticks history
    marketAPI = Market.MarketAPI(api_key, secret_key, passphrase, False, flag)
    candle_history = marketAPI.get_history_candlesticks(instId=inst_id, limit=buffer_len, bar=candlesticks_bar)
    print("[Receive the last candlesticks history]")
    # i = 0
    for data in candle_history['data']:
        candlesticks_buffer.insert(0, data[4])

    # Subscribe the current candlesticks 
    loop = asyncio.get_event_loop()
    
    loop.run_until_complete(main_loop(url, channels, candlesticks_buffer))

    loop.close()









