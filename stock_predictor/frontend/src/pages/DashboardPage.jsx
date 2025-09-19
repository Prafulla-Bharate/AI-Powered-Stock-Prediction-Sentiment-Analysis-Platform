import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import Loader from '../components/Loader';
import ErrorMessage from '../components/ErrorMessage';

const api = axios.create({
  baseURL: '/api/', // Vite proxy will handle this
  withCredentials: true,
  headers: { 'Content-Type': 'application/json' },
});

const DashboardPage = () => {
  const [watchlist, setWatchlist] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchWatchlist = async () => {
      try {
        const response = await api.get('watchlist/'); 
        setWatchlist(response.data);
      } catch (err) {
        setError("Could not fetch watchlist. Ensure you are logged into the Django Admin.");
      } finally { setLoading(false); }
    };
    fetchWatchlist();
  }, []);
  
  const handleRemove = async (id) => {
     try {
        await api.delete(`watchlist/${id}/`);
        setWatchlist(watchlist.filter(item => item.id !== id));
      } catch (err) { setError("Failed to remove item from watchlist."); }
  };

  if (loading) return <Loader />;
  if (error) return <div className="container mx-auto p-4"><ErrorMessage message={error} /></div>;

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-4xl font-bold mb-6">My Watchlist</h1>
      {watchlist.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {watchlist.map(item => (
            <div key={item.id} className="bg-gray-800 p-4 rounded-lg shadow-lg flex justify-between items-center">
              <div>
                <Link to={`/apps/${item.stock.ticker}`}>
                  <h2 className="text-2xl font-bold hover:text-blue-400">{item.stock.ticker}</h2>
                </Link>
                <p className="text-gray-400">{item.stock.company_name}</p>
              </div>
              <button onClick={() => handleRemove(item.id)} className="bg-red-600 text-white px-3 py-1 rounded hover:bg-red-700">Remove</button>
            </div>
          ))}
        </div>
      ) : (
        <div className="text-center py-10 bg-gray-800 rounded-lg">
          <p className="text-gray-400">Your watchlist is empty.</p>
        </div>
      )}
    </div>
  );
};

export default DashboardPage;
