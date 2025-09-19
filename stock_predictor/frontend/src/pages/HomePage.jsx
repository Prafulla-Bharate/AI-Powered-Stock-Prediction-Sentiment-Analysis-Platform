import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const HomePage = () => {
  const [ticker, setTicker] = useState('');
  const navigate = useNavigate();

  const handleSearch = (e) => {
    e.preventDefault();
    if (ticker.trim()) {
      navigate(`/apps/${ticker.trim().toUpperCase()}`);
    }
  };

  return (
    <div className="container mx-auto flex flex-col items-center justify-center min-h-[80vh] p-4">
      <h1 className="text-5xl font-extrabold mb-4 text-center">AI-Powered Stock Forecasting</h1>
      <p className="text-gray-400 text-lg mb-8 text-center max-w-2xl">
        Enter a stock ticker to view historical data, quantitative forecasts, and qualitative news analysis powered by Gemini.
      </p>
      <form onSubmit={handleSearch} className="w-full max-w-md">
        <div className="flex items-center bg-gray-800 border border-gray-700 rounded-lg shadow-xl overflow-hidden">
          <input
            type="text" value={ticker} onChange={(e) => setTicker(e.target.value)}
            placeholder="e.g., AAPL, GOOGL, TSLA"
            className="w-full p-4 bg-gray-800 text-white focus:outline-none"
          />
          <button type="submit" className="bg-blue-600 text-white px-6 py-4 hover:bg-blue-700 transition-colors">
            Search
          </button>
        </div>
      </form>
    </div>
  );
};

export default HomePage;