import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => (
  <nav className="bg-gray-800 p-4 shadow-lg sticky top-0 z-10">
    <div className="container mx-auto flex justify-between items-center">
      <Link to="/" className="text-2xl font-bold text-white hover:text-blue-400 transition-colors">
        Stock Predictor
      </Link>
      <div className="space-x-4">
        <Link to="/" className="text-gray-300 hover:text-white transition-colors">Home</Link>
        <Link to="/dashboard" className="text-gray-300 hover:text-white transition-colors">Dashboard</Link>
      </div>
    </div>
  </nav>
);

export default Navbar;