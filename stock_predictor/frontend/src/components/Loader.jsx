import React from 'react';

const Loader = ({ text = "Loading..." }) => (
  <div className="flex flex-col justify-center items-center h-full text-center p-10">
    <div className="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-blue-500"></div>
    <p className="mt-4 text-lg text-gray-400">{text}</p>
  </div>
);

export default Loader;