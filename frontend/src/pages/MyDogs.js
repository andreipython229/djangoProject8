import React, { useEffect, useState } from 'react';
import { fetchMyDogs } from '../api';

import tysonImg from '../assets/img/photo_2025-06-28_12-40-29.jpg';
import nihaoImg from '../assets/img/photo_2025-06-28_12-43-50.jpg';

const staticDogs = [
  { name: 'Тайсон', img: tysonImg },
  { name: 'Ни-хау', img: nihaoImg },
];

export default function MyDogs() {
  const [dogs, setDogs] = useState([]);
  const [useStatic, setUseStatic] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchMyDogs()
      .then(data => {
        if (Array.isArray(data) && data.length > 0) {
          setDogs(data);
          setUseStatic(false);
        } else {
          setUseStatic(true);
        }
        setLoading(false);
      })
      .catch(() => {
        setUseStatic(true);
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="container mt-5">Загрузка...</div>;

  const dogsToShow = useStatic ? staticDogs : dogs;

  return (
    <div className="container mt-5">
      <h1 className="text-center mb-4">Мои собаки</h1>
      <div className="row justify-content-center">
        {dogsToShow.map((dog, idx) => (
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
                src={useStatic ? dog.img : dog.image || dog.img}
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
      {useStatic && (
        <div className="text-center text-muted mt-3">
          <small>Показываю твои фотки, потому что API не отвечает или ты не залогинен</small>
        </div>
      )}
    </div>
  );
}