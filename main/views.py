from django.shortcuts import render
import requests
import json

def trade_price(url): 
    response = requests.get(url)
    response_json = response.json()
    trade_price = response_json[0]['trade_price']
    return trade_price

def index(request):
    btc_price = trade_price("https://api.upbit.com/v1/ticker?markets=KRW-BTC")
    eth_price = trade_price("https://api.upbit.com/v1/ticker?markets=KRW-ETH")
    ltc_price = trade_price("https://api.upbit.com/v1/ticker?markets=KRW-LTC")
    etc_price = trade_price("https://api.upbit.com/v1/ticker?markets=KRW-ETC")
    xrp_price = trade_price("https://api.upbit.com/v1/ticker?markets=KRW-XRP")
    bch_price = trade_price("https://api.upbit.com/v1/ticker?markets=KRW-BCH")
    eos_price = trade_price("https://api.upbit.com/v1/ticker?markets=KRW-EOS")
    ada_price = trade_price("https://api.upbit.com/v1/ticker?markets=KRW-ADA")
    qtum_price = trade_price("https://api.upbit.com/v1/ticker?markets=KRW-QTUM")
    trx_price = trade_price("https://api.upbit.com/v1/ticker?markets=KRW-TRX")
    zil_price = trade_price("https://api.upbit.com/v1/ticker?markets=KRW-ZIL")
    xlm_price = trade_price("https://api.upbit.com/v1/ticker?markets=KRW-XLM")
    
    context = {'btc_price': btc_price, 'eth_price': eth_price, 'ltc_price': ltc_price, 'etc_price': etc_price, 'xrp_price': xrp_price, 'bch_price': bch_price, 'eos_price': eos_price, 'ada_price': ada_price, 'qtum_price': qtum_price, 'trx_price': trx_price, 'zil_price': zil_price, 'xlm_price': xlm_price}
    
    return render(request, 'index.html', context)
