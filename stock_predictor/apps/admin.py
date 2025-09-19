from django.contrib import admin
from.models import Stock, StockPrice, Watchlist
# Register your models here.
admin.site.register(Stock)
admin.site.register(StockPrice)
admin.site.register(Watchlist)
