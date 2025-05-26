import React, {useState} from "react";
import MyDogsList from "./components/MyDogsList"; // путь правильный

function App() {
  const [showDogs, setShowDogs] = useState(false); // состояние для показа

  const handleClick = () => {
    setShowDogs(true); // показать список при клике
  };

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Добро пожаловать</h1>

      <button
        onClick={handleClick}
        className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded"
      >
        Мои собаки
      </button>

      {showDogs && <MyDogsList />}
    </div>
  );
}

export default App;
