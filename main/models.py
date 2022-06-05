from django.db import models

class Crypto(models.Model):
    ticker = models.CharField(max_length=50, verbose_name="코인 티커",null=True,default='')
    kr_name = models.CharField(max_length=50, verbose_name="코인 한글이름",null=True,default='')
    market = models.CharField(max_length=50, verbose_name="거래소",null=True,default='')
    price = models.CharField(max_length=50, verbose_name="코인 가격",null=True,default='')
    
    def __str__(self):
        return self.ticker

