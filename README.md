# 🚀 AI-Powered Stock Prediction & Sentiment Analysis Platform

A **full-stack web application** that leverages **Machine Learning (ML), Deep Learning (DL), and Generative AI** to provide **comprehensive stock market analysis**.  

Users can:
- View historical stock data  
- Get dual-model forecasts (**ARIMA & LSTM**)  
- Generate **real-time sentiment analysis** powered by Google Gemini on the latest financial news  

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| **Dual Forecasting Models** | Combines **ARIMA (statistical)** and **LSTM (deep learning)** for robust predictions. |
| **Generative AI News Analysis** | Integrates **Google Gemini LLM** for real-time sentiment insights (**Bullish / Bearish / Neutral**). |
| **Interactive Data Visualization** | Built with **Plotly.js**, providing dynamic, responsive, and interactive charts. |
| **User Watchlist** | Secure **token-authenticated system** allowing users to track favorite stocks. |
| **Robust Backend** | Powered by **Django REST Framework**, scalable & production-ready. |
| **Modern Frontend** | Developed using **React + Vite + TailwindCSS**, ensuring smooth SPA experience. |

---

## 🏗️ Tech Stack & Architecture

The app is **decoupled** with a REST API backend and a SPA frontend.

| Area       | Technology |
|------------|------------|
| **Backend** | Python, Django, Django REST Framework, TensorFlow/Keras, Statsmodels, Pandas, yfinance, Google Gemini API |
| **Frontend** | React.js, Vite, React Router, Tailwind CSS, Axios, Plotly.js |
| **Database** | SQLite (development) → PostgreSQL (production ready) |

---

## ⚙️ Setup & Installation

### 🔹 Prerequisites
- **Python** 3.10+  
- **Node.js** v18+ & npm  
- **Google Gemini API Key**

---

### 1️⃣ Backend Setup

```bash
# Clone the repository
git clone https://github.com/your-username/stock-predictor.git
cd stock_predictor/stock_predictor/

# Create & activate virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Add API key in .env file
echo 'GEMINI_API_KEY="YOUR_API_KEY_HERE"' > .env

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# (Optional) Fetch sample stock data
python manage.py fetch_history AAPL

# Start backend server
python manage.py runserver
```

👉 Backend runs at: **`http://127.0.0.1:8000`**

---

### 2️⃣ Frontend Setup

```bash
# Open a new terminal
cd ../frontend/

# Install dependencies
npm install

# Start frontend development server
npm start
```

👉 Frontend runs at: **`http://localhost:3000`**

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| **GET** | `/api/stocks/<ticker>/history/` | Fetch historical price data |
| **GET** | `/api/stocks/<ticker>/predict/arima/` | Get 7-day forecast (ARIMA) |
| **GET** | `/api/stocks/<ticker>/predict/lstm/` | Get 7-day forecast (LSTM) |
| **GET** | `/api/stocks/<ticker>/sentiment/` | AI-powered sentiment analysis (Gemini) |
| **GET, POST** | `/api/watchlist/` | List or add stocks to watchlist |
| **DELETE** | `/api/watchlist/<id>/` | Remove stock from watchlist |

---

## 🔐 Authentication & Watchlist

- Access **watchlist features** after logging in.  
- Login via **Django Admin**: `http://127.0.0.1:8000/admin/`  

---

## 📊 Example Workflow

1. Search for a stock ticker (e.g., **AAPL**).  
2. View **historical charts** + **predictions** (ARIMA & LSTM).  
3. Get **real-time sentiment** from financial news using Gemini AI.  
4. Add stock to your **personal watchlist**.  

 


