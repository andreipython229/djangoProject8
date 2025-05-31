import React from 'react';

function Home() {
  return (
    <div className="text-center">
      <h1 className="mb-4">Добро пожаловать в Bestdogs!</h1>
      <div className="card mx-auto" style={{ maxWidth: '500px' }}>
        <img
          src="/static/img/IMG_20231101_220024_kopiya.jpg"
          className="card-img-top rounded shadow"
          alt="Ni hao"
        />
        <div className="card-body">
          <h5 className="card-title">Ni hao 🐾</h5>
          <p className="card-text">
            Это моя собака — Ni hao. Она всегда встречает гостей первой!
          </p>
        </div>
      </div>
    </div>
  );
}

export default Home;
