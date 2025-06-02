// src/App.js
import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Header from './components/Header';

import Home from './pages/Home';
import About from './pages/About';
import Contacts from './pages/Contacts';
import MyDogs from './pages/MyDogs';
import FavoritePlaces from './pages/FavoritePlaces';
import NotFound from './pages/NotFound';

function App() {
  return (
    <>
      <Header /> {/* Навигация — теперь через Header.js */}
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
