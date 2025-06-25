import React, { useEffect, useState } from 'react';
import axios from 'axios';
import '../css/styles.css';  // Добавим стили

export default function FavoritePlaces() {
  const [places, setPlaces] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // Добавляем массив с полными, абсолютными путями к картинкам (через IP)
  const placeImages = [
    'http://192.168.100.20:8000/media/static/images/a629a148751349305bee9c1864120902_cropped_510x340.webp',
    'http://192.168.100.20:8000/media/static/images/cbbe299229e7d5c49d378287632d4deb_cropped_666x444.webp',
    'http://192.168.100.20:8000/media/static/images/d5a2bde913a14c179a94c172e5afbbb5.jpg',
    'http://192.168.100.20:8000/media/static/images/istockphoto-1482199015-1024x1024.jpg',
    'http://192.168.100.20:8000/media/static/images/pexels-charlesdeluvio-1851164.jpg',
    'http://192.168.100.20:8000/media/static/images/photo_2024-10-28_23-03-43.jpg',
  ];

  // Массив с данными о собаках для каждого места
  const dogData = [
    {
      name: "Motlik",
      age: 2,
      gender: "boy",
      image: "http://192.168.100.20:8000/media/static/images/photo_2024-10-28_23-03-43.jpg"
    },
    {
      name: "Djek",
      age: 2,
      gender: "boy",
      image: "http://192.168.100.20:8000/media/static/images/pexels-charlesdeluvio-1851164.jpg"
    },
    {
      name: "Stomik",
      age: 1,
      gender: "boy",
      image: "http://192.168.100.20:8000/media/static/images/istockphoto-1482199015-1024x1024.jpg"
    },
    {
      name: "Gerda",
      age: 3,
      gender: "girl",
      image: "http://192.168.100.20:8000/media/static/images/a629a148751349305bee9c1864120902_cropped_510x340.webp"
    },
    {
      name: "Greta",
      age: 1,
      gender: "girl",
      image: "http://192.168.100.20:8000/media/static/images/cbbe299229e7d5c49d378287632d4deb_cropped_666x444.webp"
    },
    {
      name: "Djuai",
      age: 1,
      gender: "girl",
      image: "http://192.168.100.20:8000/media/static/images/d5a2bde913a14c179a94c172e5afbbb5.jpg"
    }
  ];

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
          {places.map((place, idx) => (
            <div key={place.id} className="col-md-4 mb-4">
              <div className="card h-100">
                <img
                  src={dogData[idx].image}
                  className="card-img-top"
                  alt={dogData[idx].name}
                  style={{ height: '200px', objectFit: 'cover' }}
                />
                <div className="card-body">
                  <h5 className="card-title">{dogData[idx].name} ({dogData[idx].age} года, {dogData[idx].gender === "boy" ? "мальчик" : "девочка"})</h5>
                  <p className="card-text"><b>{place.name}</b></p>
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
