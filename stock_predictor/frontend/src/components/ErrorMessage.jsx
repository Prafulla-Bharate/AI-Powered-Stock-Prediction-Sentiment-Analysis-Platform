import React from 'react';

const ErrorMessage = ({ message }) => (
  <div className="bg-red-900/80 border border-red-700 text-white p-4 rounded-lg text-center">
    <p><strong>Error:</strong> {message}</p>
  </div>
);

export default ErrorMessage;