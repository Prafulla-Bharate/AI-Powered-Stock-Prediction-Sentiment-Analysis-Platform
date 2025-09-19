import React from 'react';
import Plot from 'react-plotly.js';

const StockChart = ({ history, arima, lstm, ticker }) => {
  if (!history || history.length === 0) return <div className="min-h-[500px] flex items-center justify-center"><p>No chart data available.</p></div>;

  const traces = [];

  traces.push({
    x: history.map(d => d.date), y: history.map(d => d.close),
    type: 'scatter', mode: 'lines', name: 'Historical Price',
    line: { color: '#17BECF', width: 2 }
  });

  if (arima && arima.length > 0) {
    traces.push({
      x: arima.map(d => d.date), y: arima.map(d => d.predicted_price),
      type: 'scatter', mode: 'lines', name: 'ARIMA Forecast',
      line: { color: '#FF7F0E', dash: 'dash' }
    });
  }
  
  if (lstm && lstm.length > 0) {
    traces.push({
      x: lstm.map(d => d.date), y: lstm.map(d => d.predicted_price),
      type: 'scatter', mode: 'lines', name: 'LSTM Forecast',
      line: { color: '#2CA02C', dash: 'dash' }
    });
  }

  return (
    <Plot
      data={traces}
      layout={{
        title: `${ticker.toUpperCase()} Price History & Forecast`,
        xaxis: { title: 'Date', color: '#f3f4f6', gridcolor: '#374151', automargin: true },
        yaxis: { title: 'Price (USD)', color: '#f3f4f6', gridcolor: '#374151', automargin: true },
        paper_bgcolor: '#1f2937', plot_bgcolor: '#1f2937',
        font: { color: '#f3f4f6' }, legend: { x: 0.01, y: 0.98 },
        margin: { l: 60, r: 30, b: 50, t: 80 },
        autosize: true
      }}
      useResizeHandler={true}
      className="w-full h-full min-h-[500px]"
    />
  );
};

export default StockChart;