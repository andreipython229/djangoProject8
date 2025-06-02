// src/components/Header.js
import React from 'react';
import { Link, useNavigate } from 'react-router-dom';

function Header() {
  const navigate = useNavigate();
  const token = localStorage.getItem('access');
  const username = localStorage.getItem('username');

  const handleLogout = () => {
    localStorage.removeItem('access');
    localStorage.removeItem('refresh');
    localStorage.removeItem('username');
    navigate('/login');
  };

  return (
    <header className="bg-dark text-white py-3 shadow">
      <div className="container d-flex justify-content-between align-items-center">
        <nav className="d-flex gap-3">
          <Link to="/" className="text-white text-decoration-none fw-bold">Главная</Link>
          <Link to="/mydogs" className="text-white text-decoration-none">Мои Собаки</Link>
          <Link to="/favorite-places" className="text-white text-decoration-none">Любимые места</Link>
        </nav>

        <div className="d-flex gap-2 align-items-center">
          {token ? (
            <>
              <span className="small">Привет, {username || 'пользователь'}!</span>
              <button onClick={handleLogout} className="btn btn-sm btn-danger">Выйти</button>
            </>
          ) : (
            <>
              <Link to="/login" className="btn btn-sm btn-primary">Войти</Link>
              <Link to="/register" className="btn btn-sm btn-success">Регистрация</Link>
            </>
          )}
        </div>
      </div>
    </header>
  );
}

export default Header;
