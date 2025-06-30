import React, { useEffect, useState } from 'react';

function Cabinet() {
  const [orders, setOrders] = useState([]);

  useEffect(() => {
    const token = localStorage.getItem('access');
    if (!token) return;
    fetch('/api/v1/orders/', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
      .then(res => res.json())
      .then(data => setOrders(data));
  }, []);

  const username = localStorage.getItem('username') || 'пользователь';

  // Функция для форматирования даты
  const formatDate = (dateStr) => {
    if (!dateStr) return '';
    const date = new Date(dateStr);
    return date.toLocaleString('ru-RU');
  };

  // Функция для подсчёта суммы заказа
  const getOrderTotal = (dogs) => {
    return dogs.reduce((sum, dog) => {
      const price = parseFloat((dog.price || '0').toString().replace(/[^\d.]/g, ''));
      return sum + (isNaN(price) ? 0 : price);
    }, 0);
  };

  return (
    <div className="container mt-4">
      <h2>Личный кабинет</h2>
      <p>Добро пожаловать, <strong>{username}</strong>!</p>
      <h4>Мои заказы:</h4>
      <ul>
        {orders.map(order => (
          <li key={order.id}>
            <div>
              <strong>Заказ #{order.id}</strong> — {formatDate(order.created_at)}<br/>
              Собаки: {order.dogs.map(d => d.name).join(', ')}<br/>
              Сумма: {getOrderTotal(order.dogs).toLocaleString('ru-RU', { style: 'currency', currency: 'RUB' })}<br/>
              Статус: {order.status}
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Cabinet;
