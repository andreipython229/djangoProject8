import React from 'react';

function Cabinet() {
  const username = localStorage.getItem('username') || 'пользователь';

  return (
    <div className="container mt-4">
      <h2>Личный кабинет</h2>
      <p>Добро пожаловать, <strong>{username}</strong>!</p>
      <p>Здесь в будущем будет история покупок, избранные собаки, настройки и прочее.</p>
    </div>
  );
}

export default Cabinet;
