import React from "react";

function Home() {
  const imageUrl = window.staticUrl + "img/IMG_20231101_220024_kopiya.jpg";

  return (
    <div className="container mt-4">
      <div className="card shadow-sm">
        <img
          src={imageUrl}
          className="card-img-top rounded-top"
          alt="Ni hao"
        />
        <div className="card-body">
          <h5 className="card-title">Добро пожаловать в Bestdogs! 🐶</h5>
          <p className="card-text">Это моя собака — Ni hao. Она всегда встречает гостей первой!</p>
        </div>
      </div>
    </div>
  );
}

export default Home;
