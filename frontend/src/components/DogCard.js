// src/components/DogCard.js
import React, { useEffect, useState } from "react";

function DogCard({ id, name, breed, age, photo }) {
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
    <div className="dog-card border p-4 rounded shadow mb-4 max-w-sm">
      <img
        src={photo || "/images/default-dog.jpg"}
        alt={name}
        className="w-full h-48 object-cover rounded"
      />
      <h3 className="mt-2 text-lg font-bold">{name}</h3>
      <p>Порода: {breed}</p>
      <p>Возраст: {age} {age === 1 ? "год" : "лет"}</p>

      <button
        onClick={handleCartToggle}
        className={`mt-2 px-3 py-1 rounded text-white ${
          inCart ? "bg-danger hover:bg-dark" : "bg-blue-500 hover:bg-blue-600"
        }`}
      >
        {inCart ? "Удалить из корзины" : "Добавить в корзину"}
      </button>
    </div>
  );
}

export default DogCard;


