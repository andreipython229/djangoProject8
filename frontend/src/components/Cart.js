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

  const handleOrder = async () => {
    const token = localStorage.getItem('access');
    if (!token) {
      alert('Сначала войдите в аккаунт!');
      return;
    }
    const dogIds = cart.map(dog => dog.id);

    try {
      const response = await fetch('/api/v1/orders/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ dogs_ids: dogIds })
      });

      if (response.ok) {
        alert('Заказ успешно оформлен!');
        localStorage.removeItem('cart');
        setCart([]);
      } else {
        alert('Ошибка при оформлении заказа');
      }
    } catch (e) {
      alert('Ошибка сети');
    }
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
      {cart.length > 0 && (
        <button className="btn btn-success mt-3" onClick={handleOrder}>
          Оформить заказ
        </button>
      )}
    </div>
  );
}

export default Cart;
