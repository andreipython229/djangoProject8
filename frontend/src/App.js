import React, {useState} from "react";
import Navbar from "./components/Navbar";
import RegisterForm from "./components/RegisterForm";

function App() {
  const [showRegisterForm, setShowRegisterForm] = useState(false);
  const [loggedIn, setLoggedIn] = useState(false);

  const handleShowRegister = () => {
    setShowRegisterForm(true);
  };

  const handleLogin = () => {
    setLoggedIn(true);
    setShowRegisterForm(false);
  };

  const handleLogout = () => {
    setLoggedIn(false);
    setShowRegisterForm(false);
  };

  return (
    <>
      <Navbar
        loggedIn={loggedIn}
        onRegisterClick={handleShowRegister}
        onLogoutClick={handleLogout}
      />
      <div className="container mt-4">
        {!loggedIn && showRegisterForm && (
          <RegisterForm onLogin={handleLogin} />
        )}
        {loggedIn && <h2>Добро пожаловать, вы вошли в систему!</h2>}
      </div>
    </>
  );
}

export default App;
