// src/components/Header.js
import React from 'react';
import { NavLink, Link, useNavigate } from 'react-router-dom';

const Header = () => {
  const navigate = useNavigate();
  const isLoggedIn = !!localStorage.getItem('access');

  const handleLogout = () => {
    localStorage.removeItem('access');
    navigate('/login/');
  };

  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
      <div className="container-fluid">
        <Link className="navbar-brand" to="/">BestDogs</Link>
        <button
          className="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav me-auto mb-2 mb-lg-0">
            <li className="nav-item">
              <NavLink className="nav-link" to="/">
                Главная
              </NavLink>
            </li>
            <li className="nav-item">
              <NavLink className="nav-link" to="/mydogs/">
                Мои Собаки
              </NavLink>
            </li>
            <li className="nav-item">
              <NavLink className="nav-link" to="/places/">
                Любимые места
              </NavLink>
            </li>
            <li className="nav-item">
              <NavLink className="nav-link" to="/about/">
                О нас
              </NavLink>
            </li>
            <li className="nav-item">
              <NavLink className="nav-link" to="/contacts/">
                Контакты
              </NavLink>
            </li>
            {isLoggedIn && (
              <>
                <li className="nav-item">
                  <NavLink className="nav-link" to="/cabinet/">
                    Личный кабинет
                  </NavLink>
                </li>
                <li className="nav-item">
                  <NavLink className="nav-link" to="/cart/">
                    Корзина
                  </NavLink>
                </li>
              </>
            )}
          </ul>
          <div className="d-flex">
            {!isLoggedIn ? (
              <>
                <Link to="/login/" className="btn btn-primary me-2">
                  Войти
                </Link>
                <Link to="/register/" className="btn btn-success">
                  Регистрация
                </Link>
              </>
            ) : (
              <button className="btn btn-outline-light" onClick={handleLogout}>
                Выйти
              </button>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Header;
