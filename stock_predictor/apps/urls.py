from django.urls import path
from .views import (
    StockListCreateAPIView,
    WatchlistListCreateAPIView,
    WatchlistDestroyAPIView,
    StockHistoryAPIView, # Import the new view
    ARIMAPredictionAPIView,
    LSTMPredictionAPIView, # Import the LSTM prediction view
    SentimentAnalysisAPIView, # Import the sentiment analysis view
)

app_name = 'apps'

urlpatterns = [
    # Endpoint for listing and creating stocks
    path('apps/', StockListCreateAPIView.as_view(), name='stock-list-create'),

    # Endpoint for getting a stock's historical data
    path('apps/<str:ticker>/history/', StockHistoryAPIView.as_view(), name='stock-history'),

    # Endpoint for managing the user's watchlist
    path('watchlist/', WatchlistListCreateAPIView.as_view(), name='watchlist-list-create'),
    path('watchlist/<int:pk>/', WatchlistDestroyAPIView.as_view(), name='watchlist-destroy'),

    path('apps/<str:ticker>/predict/arima/', ARIMAPredictionAPIView.as_view(), name='stock-predict-arima'),
    path('apps/<str:ticker>/predict/lstm/', LSTMPredictionAPIView.as_view(), name='stock-predict-lstm'),
     #  sentiment analysis URL
    path('stocks/<str:ticker>/sentiment/', SentimentAnalysisAPIView.as_view(), name='stock-sentiment'),
]