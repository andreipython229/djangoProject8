const express = require("express");

const app = express();
const port = 8000;

// Middleware для обработки JSON-запросов
app.use(express.json());

// Пример API маршрута
app.post("/api/register", (req, res) => {
  const {username, email, password} = req.body;
  // Здесь логика для обработки данных регистрации
  console.log("Данные регистрации:", {username, email, password});
  res.json({message: "User registered successfully"});
});

app.listen(port, () => {
  console.log(`API сервер запущен на порту ${port}`);
});
