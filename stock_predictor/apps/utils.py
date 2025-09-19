import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from functools import lru_cache

@lru_cache(maxsize=128)
def fetch_stock_data(ticker_symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Fetch historical stock data from yfinance.
    Caches results to minimize API calls for the same parameters.
    
    Args:
        ticker_symbol (str): Stock ticker symbol (e.g., 'AAPL').
        start_date (str): Start date in 'YYYY-MM-DD' format.
        end_date (str): End date in 'YYYY-MM-DD' format.
        
    Returns:
        pd.DataFrame: DataFrame containing historical stock data.
    """
    try:
        stock = yf.Ticker(ticker_symbol)
        history = stock.history(start=start_date, end=end_date)

        if history.empty:print(f"warning:Nodata found for {ticker_symbol} from {start_date}")

        history.reset_index(inplace=True)
        history.rename(columns={'Date': 'date', 'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Volume': 'volume'}, inplace=True)
    
        #we only need thse columns
        required_columns = ['date', 'open', 'high', 'low', 'close', 'volume']
        return history[required_columns]

    except Exception as e:
        print(f"Error fetching data for {ticker_symbol}: {e}")
        return pd.DataFrame()  # Return empty DataFrame on error
    