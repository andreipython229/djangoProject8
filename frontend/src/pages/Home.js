import React from 'react';

function Home() {
  return (
    <div className="container text-center mt-5">
      <h1 className="mb-4">Добро пожаловать в <strong>Bestdogs</strong>! 🐶</h1>

      <div className="card mx-auto shadow-lg" style={{ maxWidth: '500px' }}>
        <img
          src="/img/IMG_20231101_220024_kopiya.jpg"
          className="card-img-top rounded-top"
          alt="Ni hao"
        />
        <div className="card-body">
          <h5 className="card-title">Ni hao 🐾</h5>
          <p className="card-text">
            Это моя собака — <strong>Ni hao</strong>. Она всегда встречает гостей первой!
          </p>
          <a
            href="https://github.com/andreipython229"
            className="btn btn-outline-dark"
            target="_blank"
            rel="noopener noreferrer"
          >
            GitHub проекта
          </a>
        </div>
      </div>
    </div>
  );
}

export default Home;

