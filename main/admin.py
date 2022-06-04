from django.contrib import admin
from main.models import Crypto

class CryptoAdmin(admin.ModelAdmin):
    list_display = ('ticker', 'market',)


admin.site.register(Crypto, CryptoAdmin)