import React, { useState } from 'react';

const RegisterForm = ({ onLogin }) => {
  const [name, setName] = useState('');
  const [phone, setPhone] = useState('');
  const [error, setError] = useState('');

  const handleLogin = async () => {
    if (!name || !phone) {
      setError('Пожалуйста, заполните все поля');
      return;
    }

    try {
      const response = await fetch('/api/clients/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name, phone })
      });

      if (response.ok) {
        const data = await response.json();
        console.log('Успешно зарегистрирован клиент:', data);
        onLogin(); // вход после успешной регистрации
      } else {
        const errorData = await response.json();
        setError(`Ошибка: ${errorData.detail || 'не удалось зарегистрировать'}`);
      }
    } catch (error) {
      console.error('Ошибка при отправке запроса:', error);
      setError('Сервер недоступен');
    }
  };

  return (
    <div>
      <input
        type="text"
        className="form-control my-2"
        placeholder="Client name"
        value={name}
        onChange={(e) => setName(e.target.value)}
      />
      <input
        type="text"
        className="form-control my-2"
        placeholder="Client phone"
        value={phone}
        onChange={(e) => setPhone(e.target.value)}
      />
      <button className="btn btn-success" onClick={handleLogin}>
        Login
      </button>
      {error && <div className="alert alert-danger mt-2">{error}</div>}
    </div>
  );
};

export default RegisterForm;
