import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from datetime import date,timedelta

from statsmodels.tsa.arima.model import  ARIMA

# LSTM Imports
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense, Dropout

from.models import Stock, StockPrice

#define directory to store our trained models
BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "ml_models"
MODEL_DIR.mkdir(exist_ok=True)


def predict_with_arima(ticker: str) -> dict:
    """
    Trains an ARIMA model on the last 60 days of stock data,
    saves the model, and predicts the next 7 days.
    """
    ticker = ticker.upper()
    try:
        stock = Stock.objects.get(ticker=ticker)
        end_date = date.today()
        start_date = end_date - timedelta(days=60)
        prices_qs = StockPrice.objects.filter(
            stock=stock,
            date__range=[start_date, end_date]
        ).order_by('date')

        if prices_qs.count() < 30:
            return {"error": "Not enough data to train the model."}

        # Convert queryset to DataFrame
        data = list(prices_qs.values('date', 'close_price'))
        df = pd.DataFrame(data).set_index('date')

        # Ensure numeric dtype and handle missing values
        df['close_price'] = pd.to_numeric(df['close_price'], errors='coerce')
        df['close_price'].fillna(method='ffill', inplace=True)

        time_series = df['close_price'].astype(float)

    except Stock.DoesNotExist:
        return {"error": f"Stock with ticker {ticker} does not exist."}
    except Exception as e:
        return {"error": f"Error fetching data for ARIMA: {e}"}

    # Train and forecast
    try:
        model = ARIMA(time_series, order=(5, 1, 0))
        model_fit = model.fit()

        model_path = MODEL_DIR / f"{ticker}_arima_model.pkl"
        joblib.dump(model_fit, model_path)

        forecast = model_fit.forecast(steps=7)

        last_date = time_series.index[-1]
        forecast_dates = [last_date + timedelta(days=i) for i in range(1, 8)]

        forecast_result = {
            "ticker": ticker,
            "model_type": "ARIMA",
            "forecast": [
                {
                    "date": dt.strftime('%Y-%m-%d'),
                    "predicted_price": round(float(price), 2)
                }
                for dt, price in zip(forecast_dates, forecast)
            ]
        }
        return forecast_result

    except Exception as e:
        return {"error": f"Error training/predicting with ARIMA: {e}"}



def predict_with_lstm(ticker: str) -> dict:
    """
    Trains an LSTM model on historical stock data to predict the next 7 days.
    """
    ticker = ticker.upper()
    model_path = MODEL_DIR / f"lstm_{ticker}.h5"
    
    # --- 1. Fetch Data ---
    try:
        stock = Stock.objects.get(ticker=ticker)
        # LSTMs benefit from more data, let's try to get up to 3 years.
        end_date = date.today()
        start_date = end_date - timedelta(days=365 * 3)
        prices_qs = StockPrice.objects.filter(stock=stock, date__gte=start_date).order_by('date')
        
        if prices_qs.count() < 60: # We need at least 60 days for the sequence
            return {"error": f"Not enough historical data for LSTM. Need at least 60 days, found {prices_qs.count()}."}
        
        df = pd.DataFrame(list(prices_qs.values('date', 'close_price')))
        df.set_index('date', inplace=True)

    except Stock.DoesNotExist:
        return {"error": f"Stock with ticker {ticker} not found in the database."}
    
    # --- 2. Preprocess Data ---
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(df['close_price'].values.reshape(-1,1))
    
    prediction_days = 60 # Use last 60 days to predict
    
    X_train, y_train = [], []
    for x in range(prediction_days, len(scaled_data)):
        X_train.append(scaled_data[x-prediction_days:x, 0])
        y_train.append(scaled_data[x, 0])
        
    X_train, y_train = np.array(X_train), np.array(y_train)
    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

    # --- 3. Build and Train LSTM Model ---
    # NOTE: Training is computationally expensive and is done on every API call.
    # In production, this should be an offline process.
    model = Sequential([
        LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)),
        Dropout(0.2),
        LSTM(units=50, return_sequences=False),
        Dropout(0.2),
        Dense(units=1)
    ])
    
    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(X_train, y_train, epochs=25, batch_size=32, verbose=0) # verbose=0 to avoid printing logs
    model.save(model_path)
    
    # --- 4. Generate 7-Day Forecast ---
    last_60_days = scaled_data[-60:]
    X_test = np.reshape(last_60_days, (1, prediction_days, 1))
    
    predicted_prices = []
    
    for _ in range(7):
        predicted_stock_price = model.predict(X_test)
        predicted_prices.append(scaler.inverse_transform(predicted_stock_price)[0][0])
        
        # Update X_test to include the new prediction for the next loop
        new_sequence = np.append(X_test[0][1:], predicted_stock_price)
        X_test = np.reshape(new_sequence, (1, prediction_days, 1))

    # --- 5. Format Output ---
    last_date = df.index[-1]
    forecast_dates = [last_date + timedelta(days=i) for i in range(1, 8)]
    
    forecast_result = {
        "ticker": ticker,
        "model_type": "LSTM",
        "forecast": [
            {"date": dt.strftime('%Y-%m-%d'), "predicted_price": round(float(price), 2)}
            for dt, price in zip(forecast_dates, predicted_prices)
        ]
    }
    return forecast_result

