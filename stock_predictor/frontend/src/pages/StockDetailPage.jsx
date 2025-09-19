import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import StockChart from '../components/StockChart.jsx';
import Loader from '../components/Loader.jsx';
import ErrorMessage from '../components/ErrorMessage.jsx';

// API instance for this component
const api = axios.create({
  baseURL: '/api/', // Vite proxy will handle this
  withCredentials: true,
  headers: { 'Content-Type': 'application/json' },
});

const StockDetailPage = () => {
  const { ticker } = useParams();
  const [stockData, setStockData] = useState({ history: [], arima: [], lstm: [] });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  const [analysis, setAnalysis] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisError, setAnalysisError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true); setError(null); setAnalysis(null);
      try {
        const historyPromise = api.get(`apps/${ticker}/history/`);
        const arimaPromise = api.get(`apps/${ticker}/predict/arima/`);
        const lstmPromise = api.get(`apps/${ticker}/predict/lstm/`);
        const [historyRes, arimaRes, lstmRes] = await Promise.allSettled([historyPromise, arimaPromise, lstmPromise]);

        if (historyRes.status === 'rejected') {
          throw new Error(`Failed to fetch data for ${ticker}. Ensure the backend is running and you are logged into the Django Admin.`);
        }
        setStockData({
          history: historyRes.value.data,
          arima: arimaRes.status === 'fulfilled' ? arimaRes.value.data.forecast : [],
          lstm: lstmRes.status === 'fulfilled' ? lstmRes.value.data.forecast : [],
        });
      } catch (err) { setError(err.message || "An unexpected error occurred.");
      } finally { setLoading(false); }
    };
    fetchData();
  }, [ticker]);

  const getSentimentAnalysis = async () => {
    setIsAnalyzing(true); setAnalysisError(null); setAnalysis(null);
    try {
      const response = await api.get(`apps/${ticker}/sentiment/`);
      setAnalysis(response.data);
    } catch (err) {
      setAnalysisError(err.response?.data?.error || "Failed to get analysis. The backend might be busy or an error occurred.");
    } finally { setIsAnalyzing(false); }
  };

  const getSentimentClass = (sentiment) => {
    if (!sentiment) return 'bg-gray-500 text-gray-900';
    switch (sentiment.toLowerCase()) {
      case 'bullish': return 'bg-green-500 text-green-900';
      case 'bearish': return 'bg-red-500 text-red-900';
      default: return 'bg-gray-500 text-gray-900';
    }
  };

  if (loading) return <Loader text={`Fetching all data for ${ticker}...`} />;
  if (error) return <div className="container mx-auto p-4"><ErrorMessage message={error} /></div>;

  return (
    <div className="container mx-auto p-4 space-y-8">
      <div>
        <h1 className="text-4xl font-bold mb-2">{ticker}</h1>
        <div className="bg-gray-800 p-6 rounded-lg shadow-2xl">
          <StockChart history={stockData.history} arima={stockData.arima} lstm={stockData.lstm} ticker={ticker} />
        </div>
      </div>
      <div className="bg-gray-800 p-6 rounded-lg shadow-2xl">
        <h2 className="text-3xl font-bold mb-4">✨ AI-Powered News Analysis</h2>
        <p className="text-gray-400 mb-4">
          Click the button to use Gemini to analyze recent news and generate a real-time market sentiment summary.
        </p>
        <button onClick={getSentimentAnalysis} disabled={isAnalyzing} className="bg-purple-600 text-white px-6 py-3 rounded-lg hover:bg-purple-700 transition-colors disabled:bg-gray-600 disabled:cursor-not-allowed font-semibold">
          {isAnalyzing ? 'Analyzing...' : 'Analyze Market Sentiment'}
        </button>
        {isAnalyzing && <div className="mt-4"><Loader text="Analyzing news with Gemini..." /></div>}
        {analysisError && <div className="mt-4"><ErrorMessage message={analysisError} /></div>}
        {analysis && (
          <div className="mt-6 p-4 bg-gray-900 rounded-lg animate-fade-in">
            <h3 className="text-xl font-semibold mb-2 flex items-center">
              Sentiment: <span className={`ml-2 px-3 py-1 text-sm font-bold rounded-full ${getSentimentClass(analysis.sentiment)}`}>{analysis.sentiment || 'N/A'}</span>
            </h3>
            <p className="text-gray-300">{analysis.summary}</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default StockDetailPage;

