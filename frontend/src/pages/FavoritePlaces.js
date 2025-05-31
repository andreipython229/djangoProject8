import React, { useEffect, useState } from 'react';
import axios from 'axios';

export default function FavoritePlaces() {
  const [places, setPlaces] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    axios.get('/api/v1/places/')
      .then((response) => {
        setPlaces(response.data);
        setLoading(false);
      })
      .catch((err) => {
        setError('Ошибка при загрузке избранных мест');
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Загрузка...</p>;
  if (error) return <p className="text-danger">{error}</p>;

  return (
    <div>
      <h2>Избранные места</h2>
      {places.length === 0 ? (
        <p>Нет добавленных мест</p>
      ) : (
        <ul className="list-group">
          {places.map((place) => (
            <li key={place.id} className="list-group-item">
              <strong>{place.name}</strong> — {place.description}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
