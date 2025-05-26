import React, { useState } from "react";

function AddDogForm({ onDogAdded }) {
  const [name, setName] = useState("");
  const [breed, setBreed] = useState("");
  const [age, setAge] = useState("");
  const [price, setPrice] = useState("");
  const [errorMessage, setErrorMessage] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();

    const token = localStorage.getItem("accessToken");
    if (!token) {
      console.error("Нет access токена");
      setErrorMessage("Неавторизован");
      return;
    }

    try {
      const response = await fetch("/api/mydogs/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          name,
          breed,
          age: age === "" ? null : parseInt(age),
          price,
          category: 1, // пока жёстко, потом можно выбрать динамически
        }),
      });

      if (response.ok) {
        const newDog = await response.json();
        onDogAdded(newDog); // обновим список
        setName("");
        setBreed("");
        setAge("");
        setPrice("");
        setErrorMessage(null);
      } else {
        const errorData = await response.json();
        console.error("Ошибка при добавлении собаки:", errorData);
        setErrorMessage(
          Object.entries(errorData)
            .map(([field, errors]) => `${field}: ${errors.join(", ")}`)
            .join("; ")
        );
      }
    } catch (error) {
      console.error("Ошибка запроса:", error);
      setErrorMessage("Ошибка сети или сервера");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="mb-4 space-y-2">
      <input
        type="text"
        placeholder="Кличка"
        value={name}
        onChange={(e) => setName(e.target.value)}
        className="border p-1 w-full"
        required
      />
      <input
        type="text"
        placeholder="Порода"
        value={breed}
        onChange={(e) => setBreed(e.target.value)}
        className="border p-1 w-full"
        required
      />
      <input
        type="number"
        placeholder="Возраст"
        value={age}
        onChange={(e) => setAge(e.target.value)}
        className="border p-1 w-full"
        min="0"
        required
      />
      <input
        type="text"
        placeholder="Цена"
        value={price}
        onChange={(e) => setPrice(e.target.value)}
        className="border p-1 w-full"
        required
      />
      {errorMessage && (
        <div className="text-red-600 text-sm mb-2">{errorMessage}</div>
      )}
      <button
        type="submit"
        className="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded"
      >
        Добавить собаку
      </button>
    </form>
  );
}

export default AddDogForm;
