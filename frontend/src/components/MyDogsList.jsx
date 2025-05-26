import React, { useEffect, useState } from "react";
import AddDogForm from "./AddDogForm";

function MyDogsList() {
  const [dogs, setDogs] = useState([]);

  const fetchDogs = async () => {
    const token = localStorage.getItem("accessToken");
    if (!token) return;

    try {
      const response = await fetch("http://localhost:8000/api/mydogs/", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        setDogs(data);
      } else {
        console.error("Ошибка при получении списка собак");
      }
    } catch (error) {
      console.error("Ошибка запроса:", error);
    }
  };

  useEffect(() => {
    fetchDogs();
  }, []);

  return (
    <div>
      <h2 className="text-xl font-semibold mb-2">Мои собаки</h2>
      <AddDogForm onDogAdded={fetchDogs} />
      <ul>
        {dogs.map((dog) => (
          <li key={dog.id}>
            {dog.name} — {dog.breed} — {dog.price}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default MyDogsList;
