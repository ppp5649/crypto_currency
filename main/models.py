from django.db import models


class Crypto(models.Model):
    ticker = models.CharField(max_length=50, verbose_name="코인 이름")
    market = models.CharField(max_length=50, verbose_name="거래소")

    def __str__(self):
        return self.ticker

