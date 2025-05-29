import React, { useState } from "react";
import MyDogsList from "./components/MyDogsList";
import Header from "./components/Header";
import Footer from "./components/Footer";

function App() {
  const [showDogs, setShowDogs] = useState(false);

  const handleClick = () => {
    setShowDogs(true);
  };

  return (
    <div className="flex flex-col min-h-screen">
      <Header />

      <main className="flex-grow p-4">
        <h1 className="text-2xl font-bold mb-4">Добро пожаловать</h1>

        <button
          onClick={handleClick}
          className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded"
        >
          Мои собаки
        </button>

        {showDogs && <MyDogsList />}
      </main>

      <Footer />
    </div>
  );
}

export default App;
