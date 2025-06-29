import React from 'react';
import tysonImg from '../assets/img/photo_2025-06-28_12-40-29.jpg';
import nihaoImg from '../assets/img/photo_2025-06-28_12-43-50.jpg';

const staticDogs = [
  { name: 'Тайсон', img: tysonImg },
  { name: 'Ни-хау', img: nihaoImg },
];

export default function MyDogs() {
  return (
    <div className="container mt-5">
      <h1 className="text-center mb-4">Мои собаки</h1>
      <div className="row justify-content-center">
        {staticDogs.map((dog, idx) => (
          <div
            className="col-12 col-sm-8 col-md-6 col-lg-5 mb-4 d-flex justify-content-center"
            key={idx}
          >
            <div
              className="card h-100 shadow-sm"
              style={{
                width: '22rem',
                minHeight: '520px',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'space-between',
              }}
            >
              <img
                src={dog.img}
                className="card-img-top"
                alt={dog.name}
                style={{
                  objectFit: 'cover',
                  objectPosition: dog.name === 'Ни-хау' ? 'center' : 'top',
                  height: '480px',
                  width: '100%',
                  borderTopLeftRadius: '0.5rem',
                  borderTopRightRadius: '0.5rem',
                }}
              />
              <div className="card-body text-center" style={{ padding: '1rem' }}>
                <h5 className="card-title" style={{ margin: 0, wordBreak: 'break-word' }}>{dog.name}</h5>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}