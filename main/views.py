from django.shortcuts import render
from .models import Crypto
import requests
import json

# 매매기준율 (달러 환율)
def usd_to_krw(url):
    response = requests.get(url)
    response_json = response.json() # [{ }] -> 리스트 안에 딕셔너리 형태
    # print(response_json)  리스트 그 자체
    # print(response_json[0])  인덱스가 0 한개뿐이므로 리스트 안에있는 딕셔너리가 모두 출력
    usd_price = response_json[0]['basePrice'] # key값이 'basePrice'인 value
    
    return usd_price


# {"ticker" : 코인 한국어 이름} 형태의 dictionary 호출 함수 (업비트)
def coin_name(url):
    response = requests.get(url)
    response_json = response.json()

    name_dict = {}

    for coin in response_json:
        ticker = coin['market']
        kr_name = coin['korean_name']

        if ticker.startswith("KRW"):
            name_dict.update({ticker : kr_name})

    return name_dict

# {"ticker" : 현재가} 형태의 dictionary 호출 함수 (업비트)
def price_info(url): 
    response = requests.get(url)
    response_json = response.json()
    upbit_price = {}
    changed_rate = {}
    trade_volume = {}

    for i in range(0, len(response_json)):
        trade_price = response_json[i]['trade_price']
        market = response_json[i]['market']
        signed_change_rate = response_json[i]['signed_change_rate']
        acc_trade_price_24h = response_json[i]['acc_trade_price_24h']
        upbit_price.update({market: format(trade_price, ',')}) # 가독성을 위해 현재가 3자리마다 , 추가
        changed_rate.update({market : round(signed_change_rate, 3)}) # 변동률 소수점 3자리 제한
        trade_volume.update({market : int(acc_trade_price_24h/100000000)}) # 거래량 단위 (억)
    
    return upbit_price, changed_rate, trade_volume


def index(request):
    usd_price = usd_to_krw("https://quotation-api-cdn.dunamu.com/v1/forex/recent?codes=FRX.KRWUSD")
    name_dict = coin_name("https://api.upbit.com/v1/market/all") # 딕셔너리 형태로 코인이름 조회
    krw_tikcers = list(name_dict.keys()) # key값만 빼서 list로 조회
    str_tickers = ','.join(krw_tikcers) # url에 넣어주기 위해 list -> str 변환
    
    upbit_price, changed_rate, trade_volume = price_info(f"https://api.upbit.com/v1/ticker?markets={str_tickers}")
    context = {'usd_price' : usd_price, 'name_dict':name_dict, 'upbit_price':upbit_price, 'changed_rate':changed_rate, 'trade_volume':trade_volume,'usd_price':usd_price}

    return render(request, 'index.html', context)
