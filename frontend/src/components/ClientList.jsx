import React, { useEffect, useState } from 'react';

function ClientList() {
  const [clients, setClients] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    fetch('/api/v1/clients/')
      .then(res => {
        if (!res.ok) throw new Error('Ошибка загрузки клиентов');
        return res.json();
      })
      .then(data => setClients(data))
      .catch(err => setError(err.message));
  }, []);

  if (error) return <p style={{ color: 'red' }}>{error}</p>;

  return (
    <div>
      <h2>Список клиентов</h2>
      <ul>
        {clients.map(client => (
          <li key={client.id}>
            {client.name} — {client.phone}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default ClientList; 