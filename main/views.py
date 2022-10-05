from django.shortcuts import render
import requests
import websockets
import asyncio
import json

# 매매기준율 (달러 환율) - 두나무 api (제공사:하나은행)
def usd_to_krw(url):
    response = requests.get(url)
    response_json = response.json() # [ { } ] -> 리스트 1개 안에 딕셔너리 1개
    # print(response_json)  리스트 그 자체
    # print(response_json[0])  인덱스가 0 한개뿐이므로 리스트 안에있는 
    usd_price = response_json[0]['basePrice'] # key값이 'basePrice'인 value
    
    return usd_price


# {ticker : 한글이름} 형태의 딕셔너리 생성 함수
def get_upbit_ticker(url):
    response = requests.get(url)
    response_json = response.json() # [ {},{},{} ... ] 리스트 1개 안에 딕셔너리 ticker 개수만큼
    upbit_ticker_dict = {} # ex) {"KRW-BTC" : 비트코인}

    for coin in response_json:
        ticker = coin['market']
        kr_name = coin['korean_name']

        if ticker.startswith("KRW"):
            upbit_ticker_dict.update({ticker : kr_name})

    return upbit_ticker_dict

# 4대 거래소 시세 가져오는 함수
def get_upbit_price(url): 
    response = requests.get(url)
    response_json = response.json()
    
    # key값으로 조회도 가능하고, 템플릿 변수로 사용하기 편한 dictionary로 통일
    upbit_price = {} 
    upbit_changed_rate = {} 
    upbit_trade_volume = {} 
    
    # for문 안에 변수들은 함수 내에서만 쓰이는 변수이기 때문에 변수명 크게 신경 X
    for i in range(0, len(response_json)):
        
        trade_price = response_json[i]['trade_price'] # 현재가 
        prev_closing_price = response_json[i]['prev_closing_price'] # 전일종가(초기화 09시)
        changed_rate = ((trade_price-prev_closing_price)/prev_closing_price*100) # 변동률(직접계산)
        ticker = response_json[i]['market'] # 티커
        acc_trade_price_24h = response_json[i]['acc_trade_price_24h'] # 최근 24시간 거래량(원화)

        upbit_price.update({ticker : format(trade_price, ',')}) 
        # 현재가 3자리마다 , 추가 (단 자료형이 숫자형일 경우만 가능 str X)
        upbit_changed_rate.update({ticker : round(changed_rate, 2)})
        upbit_trade_volume.update({ticker : round(acc_trade_price_24h/100000000)})
        # float -> round로 깎고 억 단위로 나누기

    return upbit_price, upbit_changed_rate, upbit_trade_volume # return 값 다수


def get_bithumb_price(url): 
    response = requests.get(url)
    response_json = response.json()
    
    bithumb_price = {} # 빗썸 현재가 (전일 종가는 초기화 00시)
    bithumb_changed_rate = {} # 빗썸 최근 24시간 변동률 
    bithumb_trade_volume = {} # 빗썸 최근 24시간 거래량 (원화)
    data_dict = response_json['data']
    
    for ticker, price_detail in data_dict.items(): # data_dict 딕셔너리  key, value 이용
        if ticker == 'date': # date(타임 스탬프) 제외
            continue
        closing_price = price_detail['closing_price']
        fluctate_rate_24H = price_detail['fluctate_rate_24H']
        acc_trade_value_24H = round(float(price_detail['acc_trade_value_24H'])/100000000)
        # str -> float -> round로 깎고 억 단위로 나누기
        
        bithumb_price.update({ticker : format(float(closing_price), ',')})
        bithumb_changed_rate.update({ticker : fluctate_rate_24H})
        bithumb_trade_volume.update({ticker : acc_trade_value_24H })

    return bithumb_price, bithumb_changed_rate, bithumb_trade_volume


def get_coinone_price(url):
    response = requests.get(url)
    response_json = response.json()
    
    coinone_price = {}
    coinone_changed_rate = {}
    coinone_trade_volume = {}
    # 기본적으로 dictionary를 for문 돌리면 key값이 나옴
    # key값과 value값을 모두 이용하고 싶다면 
    # for key, value in dictionary.items() :
    #    print(key, value)
    for ticker,price_detail in response_json.items():
        # 불필요한 key들 제외
        if 'result' in ticker or 'errorCode' in ticker or 'timestamp' in ticker:
            continue
        last_price = float(price_detail['last'])
        yesterday_last_price = float(price_detail['yesterday_last'])
        changed_rate = round(((last_price-yesterday_last_price)/yesterday_last_price*100), 2)
        yesterday_volume = float(price_detail['yesterday_volume'])
        yesterday_volume_total = round((last_price*yesterday_volume)/100000000, 3)
        
        coinone_price.update({ticker : format(last_price, ',')})
        coinone_changed_rate.update({ticker : changed_rate})
        coinone_trade_volume.update({ticker : yesterday_volume_total})

    return coinone_price, coinone_changed_rate, coinone_trade_volume


def get_korbit_price(url):
    response = requests.get(url)
    response_json = response.json()
    
    korbit_price = {}
    korbit_changed_rate = {}
    korbit_trade_volume = {}

    for ticker,price_detail in response_json.items():
        last_price = float(price_detail['last'])
        changed_rate = price_detail['changePercent']
        trade_volume = float(price_detail['volume'])
        trade_volume_total = round((trade_volume*last_price)/100000000, 2)

        korbit_price.update({ticker : format(last_price, ',')})
        korbit_changed_rate.update({ticker : changed_rate})
        korbit_trade_volume.update({ticker : trade_volume_total})

    return korbit_price, korbit_changed_rate, korbit_trade_volume


def index(request):
    usd_price = usd_to_krw("https://quotation-api-cdn.dunamu.com/v1/forex/recent?codes=FRX.KRWUSD")
    upbit_ticker_dict = get_upbit_ticker("https://api.upbit.com/v1/market/all")     
    upbit_ticker_str = ",".join(upbit_ticker_dict) # url에 넣어주기 위해 list -> str 변환
    
    # 4대 거래소 시세 정보
    upbit_price, upbit_changed_rate, upbit_trade_volume = get_upbit_price(f"https://api.upbit.com/v1/ticker?markets={upbit_ticker_str}") 

    bithumb_price, bithumb_changed_rate, bithumb_trade_volume = get_bithumb_price("https://api.bithumb.com/public/ticker/ALL_KRW")

    coinone_price, coinone_changed_rate, coinone_trade_volume = get_coinone_price("https://api.coinone.co.kr/ticker?currency=all")

    korbit_price, korbit_changed_rate, korbit_trade_volume = get_korbit_price("https://api.korbit.co.kr/v1/ticker/detailed/all")

    # print(korbit_price)

    # 템플릿 변수
    context = {'usd_price' : usd_price, 'upbit_ticker_dict':upbit_ticker_dict, 'upbit_price':upbit_price, 'upbit_changed_rate':upbit_changed_rate, 'upbit_trade_volume':upbit_trade_volume, 'bithumb_price':bithumb_price, 'bithumb_changed_rate':bithumb_changed_rate, 'bithumb_trade_volume':bithumb_trade_volume,'coinone_price':coinone_price, 'coinone_changed_rate':coinone_changed_rate, 'coinone_trade_volume':coinone_trade_volume, 'korbit_price':korbit_price, 'korbit_changed_rate':korbit_changed_rate, 'korbit_trade_volume':korbit_trade_volume}

    return render(request, 'index.html', context)

def realtime(request):
    context = {'abc' : 'hello'}
    return render(request, "realtime.html", context)