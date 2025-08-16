import React from 'react';

export default function ProductCard({ title, oldPrice, newPrice, imageUrl, onOrderClick }) {
  return (
    <div className="max-w-sm bg-white rounded-lg shadow-md overflow-hidden">
      <img src={imageUrl} alt={title} className="w-full h-48 object-cover" />
      <div className="p-4">
        <h2 className="text-xl font-semibold mb-2">{title}</h2>
        <div className="mb-4">
          <span className="text-gray-500 line-through mr-2">{oldPrice}</span>
          <span className="text-red-600 text-lg font-bold">{newPrice}</span>
        </div>
        <div className="flex space-x-2">
          <button
            className="flex-1 bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700"
            onClick={onOrderClick}
          >
            Order Now
          </button>
          <button className="flex-1 bg-gray-200 text-gray-700 py-2 px-4 rounded hover:bg-gray-300">
            More Info
          </button>
        </div>
      </div>
    </div>
  );
}
