import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import HomePage from "./pages/HomePage";
import DashboardPage from "./pages/DashboardPage";
import StockDetailPage from "./pages/StockDetailPage";

function Footer() {
  return (
    <footer className="bg-gray-800 text-gray-400 py-6 mt-12 shadow-inner">
      <div className="container mx-auto text-center text-sm">
        <span className="font-bold text-blue-400">Stock Predictor</span> &copy;{" "}
        {new Date().getFullYear()} &mdash; Built with Django, React, and AI.{" "}
        <br />
        <span className="text-xs">
          For educational purposes only. Not financial advice.
        </span>
      </div>
    </footer>
  );
}

function App() {
  return (
    <Router>
      <div className="bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 min-h-screen flex flex-col">
        <Navbar />
        <main className="flex-1">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/stock/:ticker" element={<StockDetailPage />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}

export default App;