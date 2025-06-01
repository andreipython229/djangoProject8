import React from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import Home from './pages/Home';
import About from './pages/About';
import Contacts from './pages/Contacts';
import MyDogs from './pages/MyDogs';
import FavoritePlaces from './pages/FavoritePlaces';
import NotFound from './pages/NotFound';

function App() {
  return (
    <>
      <nav className="navbar navbar-expand-lg bg-dark px-3">
        <Link className="navbar-brand text-white" to="/">🐶 BS</Link>
        <div className="navbar-nav">
          <Link className="nav-link text-white" to="/">Home</Link>
          <Link className="nav-link text-white" to="/about">About</Link>
          <Link className="nav-link text-white" to="/contacts">Contacts</Link>
          <Link className="nav-link text-white" to="/mydogs">MyDogs</Link>
          <Link className="nav-link text-white" to="/favorite-places">Favorite Places</Link>
        </div>
      </nav>

      <div className="container mt-4">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<About />} />
          <Route path="/contacts" element={<Contacts />} />
          <Route path="/mydogs" element={<MyDogs />} />
          <Route path="/favorite-places" element={<FavoritePlaces />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </div>
    </>
  );
}

export default App;

