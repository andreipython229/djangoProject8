import React, { useEffect, useState } from "react";

function Cart() {
  const [cart, setCart] = useState([]);

  useEffect(() => {
    const stored = localStorage.getItem("cart");
    const items = stored ? JSON.parse(stored) : [];
    setCart(items);
  }, []);

  const removeFromCart = (id) => {
    const updated = cart.filter(item => item.id !== id);
    localStorage.setItem("cart", JSON.stringify(updated));
    setCart(updated);
  };

  return (
    <div className="container mt-4">
      <h2>🛒 Моя корзина</h2>
      {cart.length === 0 ? (
        <p>Корзина пуста.</p>
      ) : (
        <div className="row">
          {cart.map((dog) => (
            <div key={dog.id} className="col-md-4 mb-3">
              <div className="card">
                <img
                  src={dog.photo || "/images/default-dog.jpg"}
                  className="card-img-top"
                  alt={dog.name}
                />
                <div className="card-body">
                  <h5 className="card-title">{dog.name}</h5>
                  <p className="card-text">Порода: {dog.breed}</p>
                  <p className="card-text">Возраст: {dog.age}</p>
                  <button className="btn btn-danger" onClick={() => removeFromCart(dog.id)}>
                    Удалить
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Cart;
