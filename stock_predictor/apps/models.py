from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Stock(models.Model):
    ticker = models.CharField(max_length=10, unique=True, help_text="Stock ticker symbol")
    company_name = models.CharField(max_length=100, help_text="Full name of the company")
    sector = models.CharField(max_length=50, help_text="Sector of the company")
    last_updated = models.DateTimeField(auto_now=True, help_text="Last updated timestamp")

    def __str__(self):
        return f"{self.ticker} - {self.company_name}"
    
    class Meta:
        ordering = ['ticker']
        

class StockPrice(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='prices', help_text="Related stock")
    date = models.DateField(help_text="Date of the price record")
    open_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Opening price")
    close_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Closing price")
    high_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Highest price of the day")
    low_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Lowest price of the day")
    volume = models.BigIntegerField(help_text="Trading volume")

    def __str__(self):
        return f"{self.stock.ticker} - {self.date} - Close: {self.close_price}"
    
    class Meta:
        unique_together = ('stock', 'date')
        ordering = ['-date']

class Prediction(models.Model):

    "stores a price prediction made by machine learning model"

    ""
    MODEL_CHOICES = [
        ('ARIMA','ARIMA'),
        ('LSTM','Long Short-Term Memory'),
    ]
    
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='predictions', help_text="Related stock")
    model_type = models.CharField(max_length=10, choices=MODEL_CHOICES, help_text="Type of prediction model used")
    predicted_date = models.DateField(help_text="Date for which the price is predicted")
    predicted_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Predicted closing price")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the prediction was made")

    def __str__(self):
        return f"{self.stock.ticker} - {self.predicted_date} - Predicted: {self.predicted_price} ({self.model_type})"
    
    class Meta:
        ordering = ['-predicted_date']


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlists', help_text="User who owns the watchlist")
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='watchlisted_by', help_text="Stock added to the watchlist")
    added_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the stock was added to the watchlist")

    def __str__(self):
        return f"{self.user.username} - {self.stock.ticker}"
    
    class Meta:
        unique_together = ('user', 'stock')
        ordering = ['-added_at']