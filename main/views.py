from django.shortcuts import render
import requests
import json


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

def trade_price(url): 
    response = requests.get(url)
    response_json = response.json()
    prices = {}

    for i in range(0, len(response_json)):
        trade_price = response_json[i]['trade_price']
        market = response_json[i]['market']
        prices.update({market: trade_price})
    return prices


def index(request):
    name_dict = coin_name("https://api.upbit.com/v1/market/all") # 딕셔너리 형태로 코인이름 조회
    krw_tikcers = name_dict.keys() # key값만 빼서 ticker명만 조회
    str_tickers = ','.join(krw_tikcers) # url에 넣어주기 위해 list -> str 변환
    all_price = trade_price(f"https://api.upbit.com/v1/ticker?markets={str_tickers}")
    
    context = {'btc_price': all_price["KRW-BTC"],'eth_price': all_price["KRW-ETH"],'ltc_price': all_price["KRW-LTC"],'etc_price': all_price["KRW-ETC"],'xrp_price': all_price["KRW-XRP"],'bch_price': all_price["KRW-BCH"],'eos_price': all_price["KRW-EOS"],'ada_price': all_price["KRW-ADA"],'qtum_price': all_price["KRW-QTUM"],'trx_price': all_price["KRW-TRX"],'zil_price': all_price["KRW-ZIL"],'xlm_price': all_price["KRW-XLM"]}
    
    return render(request, 'index.html', context)
