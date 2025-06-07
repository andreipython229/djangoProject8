// src/App.js
import React from 'react';
import { Routes, Route, useNavigate } from 'react-router-dom';
import Header from './components/Header';

import Home from './pages/Home';
import About from './pages/About';
import Contacts from './pages/Contacts';
import MyDogs from './pages/MyDogs';
import FavoritePlaces from './pages/FavoritePlaces';
import NotFound from './pages/NotFound';
import LoginForm from './components/LoginForm';
import Profile from './pages/Profile';

function App() {
  const navigate = useNavigate();

  const handleLoginSuccess = (token) => {
    localStorage.setItem('access', token);
    // Если сервер возвращает имя пользователя, его можно сохранить тоже
    // Пример: localStorage.setItem('username', data.username);
    navigate('/');
  };

  return (
    <>
      <Header />
      <div className="container mt-4">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<About />} />
          <Route path="/contacts" element={<Contacts />} />
          <Route path="/mydogs" element={<MyDogs />} />
          <Route path="/favorite-places" element={<FavoritePlaces />} />
          <Route path="/login" element={<LoginForm onLoginSuccess={handleLoginSuccess} />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </div>
    </>
  );
}

export default App;
