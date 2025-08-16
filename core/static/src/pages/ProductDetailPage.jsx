import React, { useState } from 'react';
import ProductCard from '../components/ProductCard';

function BreadcrumbNav() {
  return (
    <nav className="text-sm mb-4">
      <ol className="flex space-x-2 text-gray-600">
        <li><a href="#" className="hover:underline">Home</a></li>
        <li>/</li>
        <li><a href="#" className="hover:underline">Products</a></li>
        <li>/</li>
        <li className="text-gray-800">Product Detail</li>
      </ol>
    </nav>
  );
}

function ProductHeader({ title, description }) {
  return (
    <header className="mb-6">
      <h1 className="text-3xl font-bold mb-2">{title}</h1>
      <p className="text-gray-700">{description}</p>
    </header>
  );
}

function PriceBlock({ oldPrice, newPrice }) {
  return (
    <div className="mb-6">
      <span className="text-gray-500 line-through mr-2">{oldPrice}</span>
      <span className="text-red-600 text-2xl font-bold">{newPrice}</span>
    </div>
  );
}

function OrderForm({ unitPrice }) {
  const [country, setCountry] = useState('');
  const [name, setName] = useState('');
  const [phone, setPhone] = useState('');
  const [quantity, setQuantity] = useState(1);
  const [agree, setAgree] = useState(false);

  const total = (quantity * unitPrice).toFixed(2);

  const handleSubmit = (e) => {
    e.preventDefault();
    // handle submit
  };

  return (
    <form onSubmit={handleSubmit} className="bg-gray-50 p-4 rounded shadow-md mb-10">
      <div className="mb-4">
        <label className="block text-sm font-medium mb-1">Country</label>
        <select
          value={country}
          onChange={(e) => setCountry(e.target.value)}
          className="w-full border rounded p-2"
        >
          <option value="">Select country</option>
          <option value="USA">USA</option>
          <option value="UK">UK</option>
        </select>
      </div>
      <div className="mb-4">
        <label className="block text-sm font-medium mb-1">Name</label>
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          className="w-full border rounded p-2"
        />
      </div>
      <div className="mb-4">
        <label className="block text-sm font-medium mb-1">Phone</label>
        <input
          type="tel"
          value={phone}
          onChange={(e) => setPhone(e.target.value)}
          className="w-full border rounded p-2"
        />
      </div>
      <div className="mb-4">
        <label className="block text-sm font-medium mb-1">Quantity</label>
        <div className="flex items-center">
          <button
            type="button"
            onClick={() => setQuantity((q) => Math.max(1, q - 1))}
            className="px-3 py-1 bg-gray-200"
          >
            -
          </button>
          <span className="px-4">{quantity}</span>
          <button
            type="button"
            onClick={() => setQuantity((q) => q + 1)}
            className="px-3 py-1 bg-gray-200"
          >
            +
          </button>
        </div>
        <div className="mt-2 text-sm text-gray-700">Total: ${total}</div>
      </div>
      <div className="mb-4 flex items-center">
        <input
          id="privacy"
          type="checkbox"
          checked={agree}
          onChange={(e) => setAgree(e.target.checked)}
          className="mr-2"
        />
        <label htmlFor="privacy" className="text-sm">
          I agree to the privacy policy
        </label>
      </div>
      <button
        type="submit"
        disabled={!agree}
        className="w-full bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700 disabled:opacity-50"
      >
        Submit
      </button>
    </form>
  );
}

export default function ProductDetailPage() {
  const unitPrice = 20;
  return (
    <div className="container mx-auto p-4">
      <BreadcrumbNav />
      <ProductHeader title="Sample Product" description="Short description of product" />
      <PriceBlock oldPrice="$30" newPrice="$20" />
      <OrderForm unitPrice={unitPrice} />
      <section className="mb-10">
        <h3 className="text-xl font-semibold mb-2">How it works</h3>
        <p className="text-gray-700">Explanation of how the product works.</p>
      </section>
      <section className="mb-10">
        <h3 className="text-xl font-semibold mb-2">Ingredients list</h3>
        <ul className="list-disc list-inside text-gray-700">
          <li>Ingredient 1</li>
          <li>Ingredient 2</li>
        </ul>
      </section>
      <section className="mb-10">
        <h3 className="text-xl font-semibold mb-2">Preparation tips</h3>
        <p className="text-gray-700">Tips on how to prepare the product.</p>
      </section>
      <section className="mb-10">
        <h3 className="text-xl font-semibold mb-4">Related products</h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
          <ProductCard
            title="Another Product"
            oldPrice="$25"
            newPrice="$15"
            imageUrl="https://via.placeholder.com/150"
            onOrderClick={() => {}}
          />
          <ProductCard
            title="Third Product"
            oldPrice="$40"
            newPrice="$25"
            imageUrl="https://via.placeholder.com/150"
            onOrderClick={() => {}}
          />
        </div>
      </section>
    </div>
  );
}
