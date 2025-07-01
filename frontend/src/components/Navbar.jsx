// src/components/Navbar.jsx
import React from "react";
import 'bootstrap/dist/css/bootstrap.min.css';

const Navbar = ({ loggedIn, onRegisterClick, onLogoutClick }) => {
  return (
    <nav className="navbar navbar-expand-lg bg-dark">
      <div className="container">
        <a className="navbar-brand p-0" href="/">
          <img src="/static/img/BS.png" alt="BS" width="40" />
        </a>
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
          <ul className="navbar-nav me-auto">
            <li className="nav-item">
              <a className="nav-link active text-light" href="/">Home</a>
            </li>
            <li className="nav-item">
              <a className="nav-link text-light" href="/places/">Favorite places</a>
            </li>
            {loggedIn && (
              <>
                <li className="nav-item">
                  <a className="nav-link text-light" href="/cabinet/">Личный кабинет</a>
                </li>
                <li className="nav-item">
                  <a className="nav-link text-light" href="/cart/">Корзина</a>
                </li>
              </>
            )}
          </ul>
          <ul className="navbar-nav">
            {!loggedIn ? (
              <li className="nav-item">
                <button
                  className="btn btn-outline-light"
                  onClick={onRegisterClick}
                >
                  Register / Login
                </button>
              </li>
            ) : (
              <li className="nav-item">
                <button
                  className="btn btn-outline-light"
                  onClick={onLogoutClick}
                >
                  Logout
                </button>
              </li>
            )}
          </ul>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
