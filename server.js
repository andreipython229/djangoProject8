require("dotenv").config();
const express = require("express");
const path = require("path");
const crypto = require("crypto"); // Для генерации nonce

const app = express();
const port = process.env.PORT || 3000;

// Настройка директории для статических файлов
app.use(express.static(path.join(__dirname, 'public')));

// Middleware для обработки JSON-запросов
app.use(express.json());

// Middleware для генерации nonce и добавления CSP-заголовка
app.use((req, res, next) => {
    const nonce = crypto.randomBytes(16).toString("base64"); // Генерация случайного nonce
    res.locals.nonce = nonce; // Сохраняем nonce для использования в шаблонах
    res.setHeader(
        'Content-Security-Policy',
        `default-src 'self'; script-src 'self' 'nonce-${nonce}' https://cdn.jsdelivr.net; style-src 'self' 'nonce-${nonce}' https://cdn.jsdelivr.net; img-src 'self' data:`
    );
    next();
});

// Пример API маршрута
app.post('/api/register', (req, res) => {
    const { username, email, password } = req.body;
    // Здесь логика для обработки данных регистрации
    console.log('Данные регистрации:', { username, email, password });
    res.json({ message: 'User registered successfully' });
});

// Обработчик отчетов о нарушениях CSP
app.post('/csp-violation-report-endpoint', (req, res) => {
    console.log('CSP Violation:', req.body);
    res.status(204).end();
});

// Маршрут для рендеринга главной страницы
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Добавление сервера
app.listen(port, () => {
    console.log(Сервер запущен на порту ${port});
});