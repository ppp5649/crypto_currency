# 실시간 원화거래 코인 시세 불러오기
import websockets
import asyncio
import json

async def upbit_websocket():
    
    async with websockets.connect("wss://api.upbit.com/websocket/v1", ping_interval=None) as wb:
        await wb.send('[{"ticket":"test"},{"type":"ticker", "codes":["KRW-BTC", "KRW-ETH", "KRW-LTC", "KRW-ETC", "KRW-XRP", "KRW-XLM", "KRW-BCH", "KRW-EOS", "KRW-ADA", "KRW-QTUM", "KRW-TRX", "KRW-ZIL"]}]')
        
        # 코인 목록은 코인판 사이트에서 4대 거래소 모두 상장된 코인 기준으로 코인 이름 가져옴
        # Ping Message 수정 필요 (웹 소켓 끊기는 에러)
        
        while True:
            if wb.open:
                result = await wb.recv()
                result = json.loads(result)
                price = result['trade_price']
                name = result['code']
                print(f"코인이름 : {name}")
                print(f"현재가 : {price}")
            else :
                print("연결 끊김")

loop = asyncio.get_event_loop()
asyncio.ensure_future(upbit_websocket())
loop.run_forever()

# 원화거래 코인 이름 리스트로 가져오기
# import requests

# url = "https://api.upbit.com/v1/market/all"

# response = requests.get(url)
# data = response.json()
# krw_id = []

# for coin in data:
#     coin_id = coin['market']
#     print(coin_id)

# 원화거래 코인 시세 가져오기 (실시간 X)
# import requests
# import json

# def trade_price(url): 
#     response = requests.get(url)
#     response_json = response.json()
#     trade_price = response_json[0]['trade_price']
#     return trade_price

# btc_price = trade_price("https://api.upbit.com/v1/ticker?markets=KRW-BTC")
# eth_price = trade_price("https://api.upbit.com/v1/ticker?markets=KRW-ETH")
# ltc_price = trade_price("https://api.upbit.com/v1/ticker?markets=KRW-LTC")
# etc_price = trade_price("https://api.upbit.com/v1/ticker?markets=KRW-ETC")
# xrp_price = trade_price("https://api.upbit.com/v1/ticker?markets=KRW-XRP")

# print(btc_price, etc_price, ltc_price, etc_price, xrp_price)


# tickers = ["KRW-BTC", "KRW-ETH", "KRW-LTC", "KRW-ETC", "KRW-XRP"]
# for ticker in tickers:
#     url = f"https://api.upbit.com/v1/ticker?markets={ticker}"
#     trade_price = trade_price(url)
#     print(trade_price)



# url1 = "https://api.upbit.com/v1/ticker?markets=KRW-BTC"
# url2 = "https://api.upbit.com/v1/ticker?markets=KRW-ETH"
# url3 = "https://api.upbit.com/v1/ticker?markets=KRW-LTC"
# url4 = "https://api.upbit.com/v1/ticker?markets=KRW-ETC"
# url5 = "https://api.upbit.com/v1/ticker?markets=KRW-XRP"
# response1 = requests.get(url1)
# response2 = requests.get(url2)
# response3 = requests.get(url3)
# response4 = requests.get(url4)
# response5 = requests.get(url5)
# response1_json = response1.json()
# response2_json = response2.json()
# response3_json = response3.json()
# response4_json = response4.json()
# response5_json = response5.json()
# trade_price1 = response1_json[0]['trade_price']
# trade_price2 = response2_json[0]['trade_price']
# trade_price3 = response3_json[0]['trade_price']
# trade_price4 = response4_json[0]['trade_price']
# trade_price5 = response5_json[0]['trade_price']
# print(trade_price1)
# print(trade_price2)
# print(trade_price3)
# print(trade_price4)
# print(trade_price5)