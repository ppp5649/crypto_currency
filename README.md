## 4대 거래소 내 코인들의 시세정보를 Table 형태로 보여주는 웹사이트  
### 메인페이지
<img width="947" alt="사이트 메인페이지" src="https://user-images.githubusercontent.com/59691376/172998070-3ffc3423-2317-4086-a5dc-79dd35b690f4.PNG">


### 데이터 요청 방식 
4대 거래소의 REST API을 이용하여 데이터를 요청하고 응답받은 데이터를 JSON 형태로 받아옴 (HTTP request / response 방식)  
Websocket과 ASGI를 이용하여 실시간으로 웹에 지속적인 데이터를 보내는데는 성공했지만, 내가 원하는 데이터 형태로 가공하여 보내주는데는 어려움을 겪고있어 아직 구현하지 못함


### 거래소별 특이사항
1. 변동률을 api에서 제공하지 않는 경우 현재 가격과 전일 종가를 이용하여 직접 계산함  
   이때, 가격정보를 str으로 제공하는 경우 float으로 변환하여 사용하고 float으로 제공하는 경우 그대로 사용
2. 불필요한 데이터는 if continue 구문을 통해 key값을 제외시킴 (빗썸, 코인원)
3. 코인원의 경우 ticker의 순서가 계속 바뀌며 table에 노출됨(api에서 랜덤 순서로 제공)


## 코인 시세정보 가져오는 함수의 구조 (예시 - 업비트) 
### 업비트 api 이미지
<img width="960" alt="업비트 데이터" src="https://user-images.githubusercontent.com/59691376/172998266-b2397e5f-3449-4a71-b761-9dcb2020b041.PNG">  
데이터의 형태가 list 내부에 코인 1개당 1개의 딕셔너리로 구성됨 [{BTC 시세정보}, {EOS 시세정보}, {BCH 시세정보} ...]  

그 외 나머지 거래소들은 데이터의 형태가 모두 dict이고 시세 정보를 가져오는 알고리즘이 조금씩 다름   
업비트의 경우 for문과 list 인덱싱을 이용하여 모든 코인의 데이터를 순서대로 받아 변수에 넣어줌  
이때 return 받는 변수들은 key값이 'ticker'로 통일된 딕셔너리 형태로 for문을 돌며 update함  

```python
# <main/views.py>

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

        upbit_price.update({ticker : format(trade_price, ',')}) # 현재가 3자리마다 , 추가 (단 자료형이 숫자형일 경우만 가능 str X)
        upbit_changed_rate.update({ticker : round(changed_rate, 2)})
        upbit_trade_volume.update({ticker : round(acc_trade_price_24h/100000000)}) # float -> round로 깎고 억 단위로 나누기
        
    return upbit_price, upbit_changed_rate, upbit_trade_volume # return 값 다수
 ```


## index 함수 구조
index 함수내에서 get_upbit_price 함수를 호출하여 return 받은 변수들을 선언해줌  
context에 파이썬 변수들을 넣고 (이때 파이썬 변수 하나하나가 딕셔너리) 템플릿 변수와 함께 넘겨줌

```python
# <main/views.py>

def index(request):
    upbit_ticker_dict = get_upbit_ticker("https://api.upbit.com/v1/market/all") # 모든 ticker를 dict로 가져옴 
    upbit_ticker_list = list(upbit_ticker_dict.keys()) # type을 dict_keys -> list로 변환
    upbit_ticker_str = ','.join(upbit_ticker_list) # url에 넣어주기 위해 list -> str 변환
  
    upbit_price, upbit_changed_rate, upbit_trade_volume = get_upbit_price(f"https://api.upbit.com/v1/ticker?markets={upbit_ticker_str}")
    
    context = {'upbit_ticker_dict':upbit_ticker_dict, 'upbit_price':upbit_price, 'upbit_changed_rate':upbit_changed_rate,
    'upbit_trade_volume':upbit_trade_volume}
    
    return render(request, 'index.html', context)
```


## index.html - upbit table
```html
<div class="tab-pane fade active show" id="upbit">
    <table class="table table-hover" id ="myTable-upbit" data-filter-control="true" data-show-search-clear-button="true">
      <thead>
        <tr>
          <th scope="col">코인 (Ticker)</th>
          <th scope="col">실시간 시세 (KRW)</th>
          <th scope="col">전일 대비 변동률 (%)</th>
          <th scope="col">24시간 내 거래량 (억)</th>
        </tr>
      </thead>
      <tbody>
        <!-- key와 value를 모두 이용 -->
        {% for upbit_key,upbit_value in upbit_price.items %}
        <tr>
          <!-- key를 통해 Dict 접근 getvalue 딕셔너리이름 키이름 -->
          <!-- Django 내장 filter cut을 사용하여 ticker에 있는 "KRW-" 문자열 제외 -->
          <td class="td-bold">{% getvalue upbit_ticker_dict upbit_key %} ({{upbit_key|cut:"KRW-"}})</td>
          <td>{{upbit_value}}</td>
          <td>{% getvalue upbit_changed_rate upbit_key %}</td>
          <td>{% getvalue upbit_trade_volume upbit_key %}</td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
</div>
```
