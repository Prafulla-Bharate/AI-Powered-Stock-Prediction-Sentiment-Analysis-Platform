import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from django.shortcuts import render
from rest_framework import generics, permissions , status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import  Stock, StockPrice, Watchlist
from .serializers import StockSerializer, StockPriceSerializer, WatchlistSerializer
from .utils import fetch_stock_data
from datetime import datetime, timedelta   
# Create your views here.
from django.http import HttpResponse

# Import both prediction functions
from .predictor import predict_with_arima, predict_with_lstm
from datetime import datetime, timedelta

def home(request):
    return HttpResponse("Welcome to Stock Predictor!")
# /api/stocks/ -> List all stocks or create a new one.
class StockListCreateAPIView(generics.ListCreateAPIView):
    """
    API view to retrieve a list of stocks or create a new stock.
    - GET: Returns a list of all stocks.
    - POST: Creates a new stock in the database.
    """
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [permissions.IsAuthenticated]


# /api/stocks/<ticker>/history/ -> Get historical data for a stock
# /api/stocks/<ticker>/history/ -> Get historical data for a stock
class StockHistoryAPIView(APIView):
    """
    API view to retrieve historical price data for a given stock ticker.
    It first checks the local database. If no data is found, it falls
    back to fetching from the yfinance API and stores the data.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, ticker):
        ticker = ticker.upper()
        
        try:
            stock = Stock.objects.get(ticker=ticker)
            prices = StockPrice.objects.filter(stock=stock)

            # If we have data in the DB, serve it.
            if prices.exists():
                serializer = StockPriceSerializer(prices, many=True)
                return Response(serializer.data)
            
            # If stock exists but no prices, fall through to fetch
            
        except Stock.DoesNotExist:
            # If the stock is not in our DB at all, fall through to fetch
            pass

        # Fallback: Fetch from yfinance
        print(f"No data for {ticker} in DB, fetching from yfinance...")
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365) # Fetch last year by default
        
        history_df = fetch_stock_data(ticker, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))

        if history_df.empty:
            return Response(
                {"error": f"Could not retrieve data for {ticker} from yfinance."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Get or create the stock object again, to be safe
        stock, _ = Stock.objects.get_or_create(ticker=ticker, defaults={'company_name': ticker})

        # Bulk create the new price data
        price_objects = [
            StockPrice(
                stock=stock,
                date=row['date'].date(),
                open_price=row['open'],
                high_price=row['high'],
                low_price=row['low'],
                close_price=row['close'],
                volume=row['volume']
            ) for index, row in history_df.iterrows()
        ]
        StockPrice.objects.bulk_create(price_objects, ignore_conflicts=True)

        # Retrieve the newly created data to serialize and return
        new_prices = StockPrice.objects.filter(stock=stock)
        serializer = StockPriceSerializer(new_prices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# /api/watchlist/ -> Manage the user's personal watchlist.
class WatchlistListCreateAPIView(generics.ListCreateAPIView):
    """
    API view for the user's watchlist.
    - GET: Returns the list of stocks in the current user's watchlist.
    - POST: Adds a new stock to the current user's watchlist.
    """
    serializer_class = WatchlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the watchlist items
        for the currently authenticated user.
        """
        user = self.request.user
        return Watchlist.objects.filter(user=user)

    def get_serializer_context(self):
        """
        Pass the request context to the serializer to access the user.
        """
        return {'request': self.request}


# /api/watchlist/<int:pk>/ -> Delete a stock from the watchlist.
class WatchlistDestroyAPIView(generics.DestroyAPIView):
    """
    API view to remove a stock from the user's watchlist.
    - DELETE: Removes the specified watchlist item.
    """
    serializer_class = WatchlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Ensure users can only delete their own watchlist items.
        """
        user = self.request.user
        return Watchlist.objects.filter(user=user)



# /api/stocks/<ticker>/predict/arima/ -> Get ARIMA model prediction
class ARIMAPredictionAPIView(APIView):
    """
    API view to get a 7-day stock price forecast using an ARIMA model.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, ticker):
        forecast_result = predict_with_arima(ticker)
        if "error" in forecast_result:
            return Response(forecast_result, status=status.HTTP_400_BAD_REQUEST)
        return Response(forecast_result, status=status.HTTP_200_OK)

# /api/stocks/<ticker>/predict/lstm/ -> Get LSTM model prediction
class LSTMPredictionAPIView(APIView):
    """
    API view to get a 7-day stock price forecast using an LSTM deep learning model.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, ticker):
        ticker = ticker.upper()
        
        # DISCLAIMER: LSTM model training is resource-intensive.
        # In a real-world application, this would be handled by an asynchronous
        # background worker (like Celery) and the models would be pre-trained.
        # Executing this synchronously will result in a long wait time for the user.
        
        forecast_result = predict_with_lstm(ticker)

        if "error" in forecast_result:
            return Response(forecast_result, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(forecast_result, status=status.HTTP_200_OK)

# VIEW FOR SENTIMENT ANALYSIS
class SentimentAnalysisAPIView(APIView):
    """
    An API view to get AI-powered sentiment analysis for a stock ticker using LangChain + Google Gemini (langchain-google-genai).
    """
    def get(self, request, ticker, format=None):
        # Get API key
        api_key = os.environ.get('GOOGLE_API_KEY') or os.environ.get('GEMINI_API_KEY')
        if not api_key:
            return Response(
                {"error": "Gemini (Google Generative AI) API key not configured on the server."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Optional: validate ticker
        ticker = ticker.strip().upper()
        if not ticker.isalpha():
            return Response(
                {"error": "Invalid ticker format."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Initialize model
            llm = ChatGoogleGenerativeAI(
                model="models/gemini-1.5-flash-latest",  # or whichever model you prefer
                temperature=0.0,
                google_api_key=api_key
            )

            # Build prompts
            system_message = SystemMessage(
                content=(
                    "You are a world-class financial analyst. Your task is to provide a brief market sentiment analysis "
                    "based on recent news for a given company. Your response must be a valid JSON object with two keys: "
                    "\"summary\" and \"sentiment\". The \"summary\" should be a concise, single-paragraph overview of "
                    "the key news. The \"sentiment\" must be one of three string values: \"Bullish\", \"Bearish\", or \"Neutral\". "
                    "Do not add any text, markdown formatting, or code fences outside of the JSON object."
                )
            )
            human_message = HumanMessage(
                content=f"Analyze recent news for the stock with ticker: {ticker}"
            )

            # Invoke the model
            response = llm.invoke([system_message, human_message])

            # The content should be JSON string
            content = response.content.strip()
            try:
                analysis_data = json.loads(content)
            except json.JSONDecodeError as e:
                # If parsing fails
                return Response(
                    {"error": "Model did not return valid JSON.", "model_response": content},
                    status=status.HTTP_502_BAD_GATEWAY
                )

            # Validate that required keys exist
            if "summary" not in analysis_data or "sentiment" not in analysis_data:
                return Response(
                    {"error": "JSON response missing required keys: 'summary' and/or 'sentiment'.", 
                     "model_response": analysis_data},
                    status=status.HTTP_502_BAD_GATEWAY
                )

            # Optionally enforce sentiment string in allowed list
            if analysis_data["sentiment"] not in {"Bullish", "Bearish", "Neutral"}:
                return Response(
                    {"error": "Invalid sentiment value. Must be one of: Bullish, Bearish, Neutral.",
                     "model_response": analysis_data},
                    status=status.HTTP_502_BAD_GATEWAY
                )

            return Response(analysis_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"An error occurred during sentiment analysis: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )