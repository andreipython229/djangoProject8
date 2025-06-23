import React, { useEffect, useState } from 'react';
import axios from 'axios';
import '../css/styles.css';  // Добавим стили

export default function FavoritePlaces() {
  const [places, setPlaces] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchPlaces = async () => {
      try {
        const token = localStorage.getItem('access');
        if (!token) {
          setError('Вы не авторизованы');
          setLoading(false);
          return;
        }

        const response = await axios.get('http://127.0.0.1:8000/api/v1/places/', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        
        setPlaces(response.data.results || response.data);
        setLoading(false);
        console.log('Places data:', response.data); // Добавим для отладки
      } catch (err) {
        if (err.response && err.response.status === 401) {
          setError('Ошибка аутентификации. Пожалуйста, войдите снова.');
        } else {
          setError('Ошибка при загрузке избранных мест');
        }
        setLoading(false);
        console.error('Error:', err); // Добавим для отладки
      }
    };

    fetchPlaces();
  }, []);

  if (loading) return <p>Загрузка...</p>;
  if (error) return <p className="text-danger">{error}</p>;

  return (
    <div className="container mt-4">
      <h2 className="mb-4">Избранные места</h2>
      {places.length === 0 ? (
        <p>Нет добавленных мест</p>
      ) : (
        <div className="row">
          {places.map((place) => (
            <div key={place.id} className="col-md-4 mb-4">
              <div className="card h-100">
                {place.image && (
                  <img
                    src={`http://127.0.0.1:8000/${place.image}`}
                    className="card-img-top"
                    alt={place.name}
                    style={{ height: '200px', objectFit: 'cover' }}
                    onError={(e) => {
                      console.log('Image load error:', e);
                      console.log('Image path:', place.image);
                    }}
                  />
                )}
                <div className="card-body">
                  <h5 className="card-title">{place.name}</h5>
                  <p className="card-text">
                    <small className="text-muted">{place.address}</small>
                  </p>
                  <p className="card-text">{place.description}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
