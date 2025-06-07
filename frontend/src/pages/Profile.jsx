import React from 'react';
import { useNavigate } from 'react-router-dom';

function Profile() {
  const username = localStorage.getItem('username');
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('access');
    localStorage.removeItem('refresh');
    localStorage.removeItem('username');
    navigate('/login');
  };

  return (
    <div className="container mt-4">
      <h2>Личный кабинет</h2>
      <p>Имя пользователя: {username || 'Гость'}</p>

      <button onClick={handleLogout} className="btn btn-danger mt-3">
        Выйти
      </button>
    </div>
  );
}

export default Profile;

