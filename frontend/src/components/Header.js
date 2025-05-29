import { Link } from 'react-router-dom';

export default function Header() {
  return (
    <header className="bg-gray-800 text-white px-4 py-3 shadow-md">
      <div className="max-w-6xl mx-auto flex justify-between items-center">
        <Link to="/" className="text-xl font-bold">DogShop</Link>
        <nav className="space-x-4">
          <Link to="/" className="hover:underline">Главная</Link>
          <Link to="/my-dogs" className="hover:underline">Мои собаки</Link>
          <Link to="/cart" className="hover:underline">Корзина</Link>
          <Link to="/login" className="hover:underline">Вход</Link>
          <Link to="/register" className="hover:underline">Регистрация</Link>
        </nav>
      </div>
    </header>
  );
}
