## 4대 거래소 내 코인들의 시세정보를 Table 형태로 보여주는 웹사이트
사이트 링크 : http://13.124.195.235/

### 메인페이지
<img width="947" alt="사이트 메인페이지" src="https://user-images.githubusercontent.com/59691376/172998070-3ffc3423-2317-4086-a5dc-79dd35b690f4.PNG">


### 데이터 요청 방식 
4대 거래소의 REST API를 이용하여 데이터를 요청하고 응답받은 데이터를 JSON 형태로 받아옴 (HTTP request / response 방식)  
Websocket과 ASGI를 이용하여 실시간으로 웹에 지속적인 데이터를 보내는 데는 성공했지만, 내가 원하는 데이터 형태로 가공하여 보내주는데는 어려움을 겪고 있어 아직 구현하지 못함


### 거래소별 특이사항
1. 변동률을 API에서 제공하지 않는 경우 현재 가격과 전일 종가를 이용하여 직접 계산함  
   이때, 가격정보를 str으로 제공하는 경우 float으로 변환하여 사용하고 float으로 제공하는 경우 그대로 사용
2. if continue 구문을 통해 불필요한 key값은 제외함 (빗썸, 코인원)
3. 코인원의 경우 ticker의 순서가 계속 바뀌며 table에 노출됨(API에서 랜덤 순서로 제공)


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
        upbit_changed_rate.update({ticker : round(changed_rate, 2)}) # 변동률 소수점 2자리 제한
        upbit_trade_volume.update({ticker : round(acc_trade_price_24h/100000000)}) # float -> round로 깎고 억 단위로 나누기
        
    return upbit_price, upbit_changed_rate, upbit_trade_volume # return값 다수
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
{% for key,value in dict %} 태그를 사용하여 딕셔너리 내부에서 tr태그 반복  
시세, 변동률, 거래량 모두 key값이 upbit_key로 동일하고 커스텀 템플릿 태그를 이용하여 getvalue 함수 사용

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

   
### 커스텀 템플릿 태그 
html 내에서 key값을 이용해 value 출력
```python
# <main/templatetags/custom_tag.py>

from django import template

@register.simple_tag
def getvalue(dict, key):
    return dict.get(key)   
```

## 부가 기능 - JavaScript
### 테이블 정렬(오름차순, 내림차순)
코인 이름, 시세, 변동률, 거래량에 따라 정렬 가능  

![테이블 정렬](https://user-images.githubusercontent.com/59691376/173006673-b8bfbcb1-3dd9-4264-9cfb-aec311d55414.gif)

4개 거래소 마다 모두 다른 table에 있으므로 table id값을 가져옴
```javascript
<!-- index.html -->
<script>
  new Tablesort(document.getElementById("myTable-upbit"));
  new Tablesort(document.getElementById("myTable-bithumb"));
  new Tablesort(document.getElementById("myTable-coinone"));
  new Tablesort(document.getElementById("myTable-korbit"));
</script>
```


### 코인이름으로 검색(navbar 우측)

![테이블 검색](https://user-images.githubusercontent.com/59691376/173006683-62063848-1249-4d6c-90a9-197b4ae414b8.gif)

한글 이름이나 ticker명 (td[0]) 으로 검색 가능  
검색창에 입력 한 텍스트가 포함되지 않았을 경우 tr 숨김 처리

```javascript
<!-- index.html -->
<script type="application/javascript">
  function tableSearch() {
      let input, filter, div, tr, td, txtValue;

      //Intialising Variables
      input = document.getElementById("myInput");
      filter = input.value.toUpperCase();
      div = document.getElementById("myTabContent");
      tr = div.getElementsByTagName("tr");

      for (let i = 0; i < tr.length; i++) {
          td = tr[i].getElementsByTagName("td")[0];
          if (td) {
              txtValue = td.textContent || td.innerText;
              if (txtValue.toUpperCase().indexOf(filter) > -1) {
                  tr[i].style.display = "";
              } else {
                  tr[i].style.display = "none";
              }
          }
      }
  }
</script>
```

### 페이지 리로딩
![페이지 리로딩](https://user-images.githubusercontent.com/59691376/173004781-a44037ed-5164-48c8-80c5-82a2f98ca6e4.gif)

```html
<!-- index.html -->
<li class="nav-item">
   <button onClick="window.location.reload()" class="btn btn-outline-success">Page Reloading</button>
</li>
```

## 배포 환경 : AWS - EC2 - 인스턴스
<img width="897" alt="aws 인스턴스" src="https://user-images.githubusercontent.com/59691376/173012087-b229a2d3-ae6e-431a-bebd-64b83d1acfa2.PNG">


### Webserver : Nginx - static file 선처리

/etc/nginx/sites-available/django_test  
uwsgi와 django 연결  
port : 80  
ip : 13.124.195.235  

<img width="601" alt="nginx1" src="https://user-images.githubusercontent.com/59691376/173012043-34b4ca10-5bf9-4973-b48f-efc1dc21f702.png">


/etc/nginx/nginx.conf  
uwsgi.sock 연결  

<img width="601" alt="nginx2" src="https://user-images.githubusercontent.com/59691376/173012056-e7b73127-7643-48a9-b14c-f59db1b4ac3f.png">

이때 Nginx 502 Bad Gateway 에러 발생 -> Error log 확인하여 uwsgi.sock 경로 수정 후 해결 


### WSGI : uWSGI - Nginx와 Django 연결

/etc/uwsgi/sites/uwsgi.ini  
가상환경, socket, wsgi 등 경로 입력  

<img width="327" alt="uwsgi" src="https://user-images.githubusercontent.com/59691376/173012069-2753d7c2-70f0-4c87-a78c-cb6c4a4e7080.png">

