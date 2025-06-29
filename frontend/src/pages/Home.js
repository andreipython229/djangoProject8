import React, { useEffect, useState } from 'react';
import WelcomeSection from '../components/WelcomeSection';
import { fetchMyDogs } from '../api';

const Home = () => {
  const [dogs, setDogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    console.log('Home компонент отрисован!');
    console.log('Попытка загрузить собак...');
    fetchMyDogs()
      .then(data => {
        setDogs(data);
        setLoading(false);
      })
      .catch(err => {
        setError('Ошибка при загрузке собак или вы не авторизованы');
        setLoading(false);
      });
  }, []);

  return (
    <>
      <WelcomeSection />
      <div className="container mt-5">
        <h2 className="mb-4">Все собаки</h2>
        {loading && <p>Загрузка...</p>}
        {error && <p className="text-danger">{error}</p>}
        <div className="row">
          {dogs.map((dog, idx) => (
            <div key={dog.id || idx} className="col-12 col-sm-6 col-md-4 col-lg-3 mb-4 d-flex justify-content-center">
              <div className="card h-100 shadow-sm" style={{ width: '18rem', minHeight: '350px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
                {/* Показываем картинку только если есть dog.image */}
                {dog.image && dog.image.trim() !== '' && (
                  <img
                    src={dog.image}
                    className="card-img-top"
                    alt={dog.name}
                    style={{ objectFit: 'cover', height: '220px', width: '100%', borderTopLeftRadius: '0.5rem', borderTopRightRadius: '0.5rem' }}
                  />
                )}
                <div className="card-body text-center" style={{ padding: '1rem' }}>
                  <h5 className="card-title" style={{ margin: 0, wordBreak: 'break-word' }}>{dog.name}</h5>
                  <p className="card-text mb-1">Порода: {dog.breed}</p>
                  <p className="card-text mb-1">Возраст: {dog.age}</p>
                  <p className="card-text mb-1">Цена: {dog.price}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </>
  );
};

export default Home;