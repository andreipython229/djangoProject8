import React, { useState } from "react";
import Header from "./components/Header";
import Footer from "./components/Footer";
import DogList from "./components/DogList";

function App() {
  const [showDogs, setShowDogs] = useState(false);

  return (
    <div className="flex flex-col min-h-screen">
      <Header />

      <main className="flex-grow p-4">
        <h1 className="text-2xl font-bold mb-4">Добро пожаловать</h1>

        <button
          onClick={() => setShowDogs(true)}
          className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded"
        >
          Мои собаки
        </button>

        {showDogs && <DogList />}
      </main>

      <Footer />
    </div>
  );
}

export default App;
