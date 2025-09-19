from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Stock, StockPrice, Watchlist

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['id', 'ticker', 'company_name', 'sector', 'last_updated']

class StockPriceSerializer(serializers.ModelSerializer):

    class Meta:
        model = StockPrice
        fields = [ 'date', 'open_price', 'close_price', 'high_price', 'low_price', 'volume']


class WatchlistSerializer(serializers.ModelSerializer):
    stock = StockSerializer(read_only=True)

    class Meta:
        model = Watchlist
        fields = ['id', 'stock','stock_id', 'added_at']
        read_only_fields = ['id', 'added_at']

    def create(self, validated_data):
        """
        Override the create method to associate the watchlist item with the
        logged-in user.
        """
        user = self.context['request'].user
        stock_id = validated_data.pop('stock_id')
        
        # Check if the stock exists
        try:
            stock = Stock.objects.get(id=stock_id)
        except Stock.DoesNotExist:
            raise serializers.ValidationError("Stock with this ID does not exist.")

        # Create the watchlist item
        watchlist_item, created = Watchlist.objects.get_or_create(
            user=user,
            stock=stock,
            defaults=validated_data
        )

        if not created:
            raise serializers.ValidationError("This stock is already in your watchlist.")
            
        return watchlist_item