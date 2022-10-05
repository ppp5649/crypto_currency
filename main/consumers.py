from channels.generic.websocket import AsyncWebsocketConsumer
from asyncio import sleep
import requests
import json


class MainConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        while True:
            korbit_price, korbit_changed_rate, korbit_trade_volume = get_korbit_price("https://api.korbit.co.kr/v1/ticker/detailed/all")
            await self.send(json.dumps({'value1':korbit_price['btc_krw'], 'value2': korbit_changed_rate['btc_krw']}))
            # dumps() : dict 형태였던 json을 str 으로 바꿔줌
            await sleep(2)


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