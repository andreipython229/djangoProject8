import React from 'react';
import { Link } from 'react-router-dom';

export default function NotFound() {
  return (
    <div className="min-h-screen bg-white flex flex-col items-center justify-center text-center px-4">
      <h1 className="text-6xl font-bold text-red-600 mb-4">404</h1>
      <h2 className="text-2xl font-semibold text-gray-800 mb-2">Страница не найдена</h2>
      <p className="text-gray-600 mb-6">
        Извините, такой страницы не существует. Проверьте адрес или вернитесь на главную.
      </p>
      <Link to="/" className="text-blue-500 hover:underline text-lg">
        ⬅ На главную
      </Link>
    </div>
  );
}

