import React, { useEffect, useState } from 'react';
import WelcomeSection from '../components/WelcomeSection';
import { fetchMyDogs } from '../api';
import DogCard from '../components/DogCard';

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
              <DogCard
                id={dog.id}
                name={dog.name}
                breed={dog.breed}
                age={dog.age}
                photo={dog.image}
                price={dog.price}
                gender={dog.gender}
              />
            </div>
          ))}
        </div>
      </div>
    </>
  );
};

export default Home;