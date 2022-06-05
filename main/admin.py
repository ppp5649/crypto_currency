from django.contrib import admin
from main.models import Crypto

class CryptoAdmin(admin.ModelAdmin):
    list_display = ('ticker','kr_name', 'market','price')


admin.site.register(Crypto, CryptoAdmin)