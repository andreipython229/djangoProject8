// src/components/DogCard.js
import React, { useEffect, useState } from "react";

function DogCard({ id, name, breed, age, photo, price, gender }) {
  const [inCart, setInCart] = useState(false);

  // Проверка при загрузке компонента
  useEffect(() => {
    const stored = localStorage.getItem("cart");
    const cart = stored ? JSON.parse(stored) : [];
    const exists = cart.some((item) => item.id === id);
    setInCart(exists);
  }, [id]);

  const handleCartToggle = () => {
    const stored = localStorage.getItem("cart");
    const cart = stored ? JSON.parse(stored) : [];

    if (inCart) {
      // Удалить из корзины
      const updatedCart = cart.filter((item) => item.id !== id);
      localStorage.setItem("cart", JSON.stringify(updatedCart));
      setInCart(false);
    } else {
      // Добавить в корзину
      cart.push({ id, name, breed, age, photo });
      localStorage.setItem("cart", JSON.stringify(cart));
      setInCart(true);
    }
  };

  return (
    <div
      className="card h-100 shadow-sm"
      style={{
        width: '18rem',
        minHeight: '370px',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'space-between',
        background: '#fff',
        borderRadius: '0.5rem',
      }}
    >
      <img
        src={photo || "/images/default-dog.jpg"}
        alt={name}
        className="card-img-top"
        style={{
          objectFit: 'cover',
          height: '220px',
          width: '100%',
          borderTopLeftRadius: '0.5rem',
          borderTopRightRadius: '0.5rem',
        }}
      />
      <div className="card-body text-center" style={{ padding: '1rem' }}>
        <h5 className="card-title" style={{ margin: 0, wordBreak: 'break-word' }}>{name}</h5>
        <p className="card-text mb-1">Порода: {breed}</p>
        <p className="card-text mb-1">Возраст: {age} {age === 1 ? "год" : "лет"}</p>
        {gender && (
          <p className="card-text mb-1">Пол: {gender === 'male' ? 'мальчик' : 'девочка'}</p>
        )}
        {price !== undefined && <p className="card-text mb-1">Цена: {price}</p>}
        <button
          onClick={handleCartToggle}
          className={`mt-2 btn ${inCart ? "btn-danger" : "btn-primary"}`}
        >
          {inCart ? "Удалить из корзины" : "Добавить в корзину"}
        </button>
      </div>
    </div>
  );
}

export default DogCard;


