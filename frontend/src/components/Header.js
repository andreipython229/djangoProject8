// src/components/Header.js
import React from 'react';
import { NavLink, Link } from 'react-router-dom';

const Header = () => {
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
          </ul>
          <div className="d-flex">
            <Link to="/login/" className="btn btn-primary me-2">
              Войти
            </Link>
            <Link to="/register/" className="btn btn-success">
              Регистрация
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Header;
