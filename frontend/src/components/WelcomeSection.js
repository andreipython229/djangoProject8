import React from 'react';
import { Link } from 'react-router-dom';
import '../css/WelcomeSection.css'; // Будет создан позже

// Внимание: URL изображения будет отличаться в зависимости от того, как вы его обслуживаете в React
// Если Django StaticFiles используется для отдачи, то путь будет как в Django шаблоне
// Если это локальный импорт в React, то путь должен быть относительным к этому файлу
// Для простоты, пока будем использовать путь, как будто Django его отдаёт
// Если React собирает статические файлы, то изображение должно быть импортировано

// Временное решение: использовать путь, который React Build сделает доступным
// Если изображение находится в src/assets/img, то можно импортировать:
// import niHaoDogImage from '../assets/img/IMG_20231101_220024_kopiya.jpg';
// Но поскольку оно было в static, предполагаем, что это будет относительный путь к корню статики
// Давайте временно используем статический URL, предполагая, что Django отдаст его
// В реальном React-приложении, если изображение лежит в src/assets, его нужно импортировать.
// Для простоты, пока используем статичный путь, который Django будет обслуживать через MEDIA_URL или STATIC_URL.
// Либо будем использовать заглушку. Давайте предположим, что `window.staticUrl` будет доступен.

function WelcomeSection() {
  const niHaoDogImage = window.staticUrl ? `${window.staticUrl}img/IMG_20231101_220024_kopiya.jpg` : '/static/img/IMG_20231101_220024_kopiya.jpg';

  return (
    <div className="welcome-container">
      <h1 className="mb-3">Добро пожаловать в Bestdogs! 🐶</h1>

      <img
        src={niHaoDogImage}
        alt="собака"
        className="welcome-image"
      />

      <p className="mt-3 text-muted fs-5">
        Это моя собака — Ni hao. Она всегда встречает гостей первой!
      </p>

      {/* 🔹 Кнопки "Войти" и "Регистрация" */}
      <div className="d-flex justify-content-center gap-3 mt-4">
        <Link to="/login" className="btn btn-primary">Войти</Link>
        <Link to="/register" className="btn btn-outline-primary">Регистрация</Link>
      </div>
    </div>
  );
}

export default WelcomeSection; 