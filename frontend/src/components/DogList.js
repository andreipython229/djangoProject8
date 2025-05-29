// src/components/DogList.js
import React, { useEffect, useState } from "react";
import DogCard from "./DogCard";

function DogList() {
  const [dogs, setDogs] = useState([]);

  useEffect(() => {
    const token = localStorage.getItem("accessToken");
    if (!token) return;

    fetch("http://localhost:8000/api/mydogs/", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then((res) => {
        if (!res.ok) throw new Error("Ошибка загрузки собак");
        return res.json();
      })
      .then((data) => setDogs(data))
      .catch((err) => console.error(err));
  }, []);

  return (
    <div>
      <h2 className="text-xl font-semibold mb-4">Мои собаки</h2>
      {dogs.length === 0 ? (
        <p>Собаки не найдены</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {dogs.map((dog) => (
            <DogCard
              key={dog.id}
              name={dog.name}
              breed={dog.breed}
              age={dog.age}
              photo={dog.photo}
            />
          ))}
        </div>
      )}
    </div>
  );
}

export default DogList;
