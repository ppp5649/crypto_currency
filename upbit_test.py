# views에 넣기 전 테스트 페이지(시행착오들이 모두 담겨있음)

# 실시간 원화거래 코인 시세 불러오기 (websocket)
# import websockets
# import asyncio
# import json

# async def upbit_websocket():
    
#     async with websockets.connect("wss://api.upbit.com/websocket/v1", ping_interval=None) as websocket:
#         await websocket.send('[{"ticket":"test"},{"type":"ticker", "codes":["KRW-BTC"]}]')
        
#         # 코인 목록은 코인판 사이트에서 4대 거래소 모두 상장된 코인 기준으로 코인 이름 가져옴
#         # Ping Message 수정 필요 (웹 소켓 끊기는 에러)
        
#         while True:
#             if websocket.open:
#                 result = await websocket.recv()
#                 result = json.loads(result)
#                 price = result['trade_price']
#                 name = result['code']
#                 print(f"코인이름 : {name}")
#                 print(f"현재가 : {price}")
#             else :
#                 print("연결 끊김")

# loop = asyncio.get_event_loop()
# asyncio.ensure_future(upbit_websocket())
# loop.run_forever()

# 코인 이름 가져오기
# import requests

# url = "https://api.upbit.com/v1/market/all"

# response = requests.get(url)
# data = response.json()
# krw_id = []

# for coin in data:
#     coin_id = coin['market']
#     print(coin_id)

# 원화 거래 코인만 리스트로 가져오기
# import requests

# url = "https://api.upbit.com/v1/market/all"

# resp = requests.get(url)
# data = resp.json()

# krw_tickers = []

# for coin in data:
#     ticker = coin['market']

#     if ticker.startswith("KRW"):
#         krw_tickers.append(ticker)
        
# print(krw_tickers)

# ticker와 코인 이름 dictionary로 가져오기    
# url = "https://api.upbit.com/v1/market/all"
# response = requests.get(url)
# response_json = response.json()

# name_dict = {}

# for coin in response_json:
#     ticker = coin['market']
#     kr_name = coin['korean_name']

#     if ticker.startswith("KRW"):
#         name_dict.update({ticker : kr_name})

# krw_tikcers = name_dict.keys()
# str_tickers = ','.join(krw_tikcers)

# 원화거래 코인 시세 가져오기 (실시간 X)
# import requests
# import json

# def trade_price(url): 
#     response = requests.get(url)
#     response_json = response.json()
#     prices = {}

#     for i in range(0, len(response_json)):
#         trade_price = response_json[i]['trade_price']
#         market = response_json[i]['market']
#         prices.update({market: trade_price})
#     return prices

# tickers = "KRW-BTC,KRW-ETH,KRW-LTC,KRW-ETC,KRW-XRP"
# all_price = trade_price("https://api.upbit.com/v1/ticker?markets=KRW-BTC, KRW-ETH, KRW-NEO, KRW-MTL, KRW-LTC, KRW-XRP, KRW-ETC, KRW-OMG, KRW-SNT, KRW-WAVES, KRW-XEM, KRW-QTUM, KRW-LSK, KRW-STEEM, KRW-XLM, KRW-ARDR, KRW-ARK, KRW-STORJ, KRW-GRS, KRW-REP, KRW-ADA, KRW-SBD, KRW-POWR, KRW-BTG, KRW-ICX, KRW-EOS, KRW-TRX, KRW-SC, KRW-ONT, KRW-ZIL, KRW-POLY, KRW-ZRX, KRW-LOOM, KRW-BCH, KRW-BAT, KRW-IOST, KRW-RFR, KRW-CVC, KRW-IQ, KRW-IOTA, KRW-MFT, KRW-ONG, KRW-GAS, KRW-UPP, KRW-ELF, KRW-KNC, KRW-BSV, KRW-THETA, KRW-QKC, KRW-BTT, KRW-MOC, KRW-ENJ, KRW-TFUEL, KRW-MANA, KRW-ANKR, KRW-AERGO, KRW-ATOM, KRW-TT, KRW-CRE, KRW-MBL, KRW-WAXP, KRW-HBAR, KRW-MED, KRW-MLK, KRW-STPT, KRW-ORBS, KRW-VET, KRW-CHZ, KRW-STMX, KRW-DKA, KRW-HIVE, KRW-KAVA, KRW-AHT, KRW-LINK, KRW-XTZ, KRW-BORA, KRW-JST, KRW-CRO, KRW-TON, KRW-SXP, KRW-HUNT, KRW-PLA, KRW-DOT, KRW-SRM, KRW-MVL, KRW-STRAX, KRW-AQT, KRW-GLM, KRW-SSX, KRW-META, KRW-FCT2, KRW-CBK, KRW-SAND, KRW-HUM, KRW-DOGE, KRW-STRK, KRW-PUNDIX, KRW-FLOW, KRW-DAWN, KRW-AXS, KRW-STX, KRW-XEC, KRW-SOL, KRW-MATIC, KRW-NU, KRW-AAVE, KRW-1INCH, KRW-ALGO, KRW-NEAR, KRW-WEMIX, KRW-AVAX, KRW-T, KRW-CELO, KRW-GMT")
# btc_price = trade_price("https://api.upbit.com/v1/trades/ticks?market=KRW-BTC&count=1")
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

# 코인 이름 함수로 불러오기

# import requests
# import json

# def coin_name(url):
#     response = requests.get(url)
#     response_json = response.json()

#     krw_tikcers = {}

#     for coin in response_json:
#         ticker = coin['market']
#         kr_name = coin['korean_name']

#         if ticker.startswith("KRW"):
#             krw_tikcers.update({ticker : kr_name})

#     return krw_tikcers

# coin_name = coin_name("https://api.upbit.com/v1/market/all")
# print(coin_name)
# print(coin_name['KRW-BTC'])

# 하나은행 환율 정보
# import requests
# import json

# response = requests.get("https://quotation-api-cdn.dunamu.com/v1/forex/recent?codes=FRX.KRWUSD")
# response_json = response.json() # [{ }] -> 리스트 안에 딕셔너리 형태
# print(response_json) # 리스트
# print(response_json[0]) # 인덱스가 0 한개뿐이므로 리스트 안에있는 딕셔너리가 모두 출력
# print(response_json[0]['basePrice'])

# import requests

# def bithumb_price(url): 
#     response = requests.get(url)
#     response_json = response.json()
#     data = response_json['data']
#     prices = {}

#     for coin in data:
#         print(coin)

#     return prices

# 빗썸 시세 가져오기
# bithumb_price = bithumb_price("https://api.bithumb.com/public/ticker/all_krw")
# print(bithumb_price)

# import requests

# def get_bithumb_price(url): 
#     response = requests.get(url)
#     response_json = response.json()
#     bithumb_price = {}

#     data = response_json['data']
#     for coin in data.keys():
#         if coin == 'date': # date(날짜코드) 제외
#             continue
#         values = data[coin]
#         bithumb_price.update({coin: values['closing_price']})
#     return bithumb_price

# 코인원 시세 가져오기
# import requests

# response = requests.get("https://api.coinone.co.kr/ticker?currency=all")
# response_json = response.json()
# coinone_price = {}

# # 기본적으로 dictionary를 for문 돌리면 key값이 나옴
# # key값과 value값을 모두 이용하고 싶다면 
# # for key, value in dictionary.items() :
# #    print(key, value)
# for ticker,price_detail in response_json.items():
#     # 불필요한 key들 제외
#     if 'result' in ticker or 'errorCode' in ticker or 'timestamp' in ticker:
#         continue
#     last_price = price_detail['last']
#     coinone_price.update({ticker : last_price})

# print(coinone_price)

# 코빗 시세 가져오기
# import requests

# response = requests.get("https://api.korbit.co.kr/v1/ticker/detailed/all")
# response_json = response.json()
# korbit_price = {}
# korbit_changed_rate = {}
# korbit_trade_volume = {}

# for ticker,price_detail in response_json.items():
#     last_price = float(price_detail['last'])
#     changed_rate = price_detail['changePercent']
#     trade_volume = float(price_detail['volume'])
#     trade_volume_total = round((trade_volume*last_price)/100000000, 2)

#     korbit_price.update({ticker : last_price})
#     korbit_changed_rate.update({ticker : changed_rate})
#     korbit_trade_volume.update({ticker : trade_volume_total})

# print(korbit_trade_volume)

# 빗썸 시세 가져오기(통일감 있게 수정) - 딕셔너리 value 값 이용 방법 변경
# import requests

# response = requests.get("https://api.bithumb.com/public/ticker/all_krw")
# response_json = response.json()
# bithumb_price = {} # 빗썸 현재가 (전일 종가는 초기화 00시)
# bithumb_changed_rate = {} # 빗썸 최근 24시간 변동률 
# bithumb_trade_volume = {} # 빗썸 최근 24시간 거래량 (원화)
# data_dict = response_json['data']

# for ticker, price_detail in data_dict.items(): # data_dict 딕셔너리 
#     if ticker == 'date': # date(타임 스탬프) 제외
#         continue
#     closing_price = price_detail['closing_price']
#     fluctate_rate_24H = price_detail['fluctate_rate_24H']
#     acc_trade_value_24H = round(float(price_detail['acc_trade_value_24H'])/100000000)
#     # str -> float -> round로 깎고 억 단위로 나누기
    
#     bithumb_price.update({ticker : closing_price})
#     bithumb_changed_rate.update({ticker : fluctate_rate_24H})
#     bithumb_trade_volume.update({ticker : acc_trade_value_24H })

# print(bithumb_trade_volume)