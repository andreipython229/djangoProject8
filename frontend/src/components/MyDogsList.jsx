import React, { useEffect, useState } from "react";

function MyDogsList() {
  const [dogs, setDogs] = useState([]);

  useEffect(() => {
    const fetchDogs = async () => {
      const token = localStorage.getItem("accessToken");
      if (!token) return;

      try {
        const response = await fetch("/api/mydogs/", {
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

    fetchDogs();
  }, []);

  return (
    <div>
      <h2>Мои собаки</h2>
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
