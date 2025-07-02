import React, { useEffect, useState } from 'react';
import { fetchOrders } from '../api';

function Cabinet() {
  const username = localStorage.getItem('username') || 'пользователь';
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchOrders()
      .then(data => {
        setOrders(data);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  return (
    <div className="container mt-4">
      <h2>Личный кабинет</h2>
      <p>Добро пожаловать, <strong>{username}</strong>!</p>
      <h4 className="mt-4">История заказов</h4>
      {loading && <p>Загрузка заказов...</p>}
      {error && <p className="text-danger">Ошибка: {error}</p>}
      {!loading && !error && orders.length === 0 && <p>У вас пока нет заказов.</p>}
      {!loading && !error && orders.length > 0 && (
        <div className="mt-3">
          {orders.map(order => (
            <div key={order.id} className="border rounded p-3 mb-3 bg-light">
              <div><strong>Заказ №{order.id}</strong> от {new Date(order.created_at).toLocaleString()}</div>
              <div>Статус: {order.status}</div>
              <div>Собаки в заказе:
                <ul>
                  {order.dogs && order.dogs.length > 0 ? order.dogs.map(dog => (
                    <li key={dog.id || dog}>
                      {dog.name || dog}
                      {dog.owner ? (
                        <span className="text-muted ms-2">(Владелец: {dog.owner})</span>
                      ) : null}
                    </li>
                  )) : <li>Нет данных</li>}
                </ul>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Cabinet;
