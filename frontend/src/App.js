import React, {useState, useEffect} from "react";
import LoginForm from "./components/LoginForm";
import {fetchMyDogs} from "./api";

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(
    !!localStorage.getItem("accessToken")
  );
  const [dogs, setDogs] = useState([]);
  const [error, setError] = useState(null);

  const handleLoginSuccess = (accessToken) => {
    localStorage.setItem("accessToken", accessToken);
    setIsAuthenticated(true);
  };

  useEffect(() => {
    if (isAuthenticated) {
      fetchMyDogs()
        .then((data) => {
          setDogs(data);
          setError(null);
        })
        .catch((err) => {
          setError(err.message);
          // можно по ошибке 401 очистить токен и выйти из аккаунта
          if (err.message.includes("Неавторизован")) {
            localStorage.removeItem("accessToken");
            setIsAuthenticated(false);
          }
        });
    }
  }, [isAuthenticated]);

  if (!isAuthenticated) {
    return <LoginForm onLoginSuccess={handleLoginSuccess} />;
  }

  return (
    <div>
      <h1>Мои собаки</h1>
      {error && <div style={{color: "red"}}>{error}</div>}
      <ul>
        {dogs.map((dog) => (
          <li key={dog.id}>
            {dog.name} ({dog.breed})
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
