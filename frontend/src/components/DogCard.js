// src/components/DogCard.js
import React from "react";

function DogCard({ name, breed, age, photo }) {
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
      <button className="mt-2 bg-blue-500 text-white px-3 py-1 rounded hover:bg-blue-600">
        Добавить в корзину
      </button>
    </div>
  );
}

export default DogCard;


