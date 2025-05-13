require("dotenv").config();
const express = require("express");
const path = require("path");
const crypto = require("crypto");
const cookieParser = require('cookie-parser');

const app = express();
const port = process.env.PORT || 3000;
const cookieDomain = process.env.COOKIE_DOMAIN || 'localhost';
const isDevelopment = process.env.NODE_ENV === 'development';
const sslEnabled = process.env.SSL_ENABLED === 'True';

// Базовые настройки безопасности
app.disable('x-powered-by');
app.set('trust proxy', 1);

// Middleware для проверки версии HTTP
app.use((req, res, next) => {
    if (req.httpVersion !== '1.1' && req.httpVersion !== '2.0') {
        return res.status(400).json({
            error: {
                message: 'Unsupported HTTP version',
                status: 400
            }
        });
    }
    next();
});

// Middleware для проверки заголовков
app.use((req, res, next) => {
    if (!req.headers['content-type'] && req.method !== 'GET') {
        return res.status(400).json({
            error: {
                message: 'Content-Type header is required',
                status: 400
            }
        });
    }
    next();
});

// Настройка директории для статических файлов
app.use(express.static(path.join(__dirname, "public")));

// Middleware для обработки JSON-запросов с ограничением размера
app.use(express.json({
    limit: '10kb',
    verify: (req, res, buf) => {
        try {
            JSON.parse(buf);
        } catch (e) {
            res.status(400).json({
                error: {
                    message: 'Invalid JSON',
                    status: 400
                }
            });
        }
    }
}));

app.use(express.urlencoded({
    extended: true,
    limit: '10kb',
    verify: (req, res, buf) => {
        if (buf.length > 10240) { // 10kb
            res.status(413).json({
                error: {
                    message: 'Request entity too large',
                    status: 413
                }
            });
        }
    }
}));

app.use(cookieParser());

// Enable CORS с дополнительными настройками безопасности
app.use((req, res, next) => {
    // В режиме разработки разрешаем все источники
    const allowedOrigin = isDevelopment ? '*' : `https://${cookieDomain}`;
    res.header('Access-Control-Allow-Origin', allowedOrigin);
    res.header('Access-Control-Allow-Credentials', 'true');
    res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
    res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept, Authorization');
    res.header('X-Content-Type-Options', 'nosniff');
    res.header('X-Frame-Options', 'DENY');
    res.header('X-XSS-Protection', '1; mode=block');

    // Добавляем HSTS заголовки как в Django (SECURE_HSTS_SECONDS = 31536000)
    if (sslEnabled) {
        res.header('Strict-Transport-Security', 'max-age=31536000; includeSubDomains; preload');
    }

    // Обработка preflight запросов
    if (req.method === 'OPTIONS') {
        return res.status(200).end();
    }
    next();
});

// Cookie configuration middleware с настройками как в Django
app.use((req, res, next) => {
    try {
        // Настройки для сессионных куков (SESSION_COOKIE_SECURE = False)
        res.cookie('session', 'your-session-value', {
            secure: false,      // Соответствует SESSION_COOKIE_SECURE = False
            httpOnly: true,     // Соответствует SESSION_COOKIE_HTTPONLY = True
            sameSite: 'Lax',    // Соответствует SESSION_COOKIE_SAMESITE = 'Lax'
            maxAge: 24 * 60 * 60 * 1000,
            path: '/',
            domain: cookieDomain
        });

        // Настройки для CSRF куков (CSRF_COOKIE_SECURE = True)
        res.cookie('csrftoken', crypto.randomBytes(32).toString('hex'), {
            secure: true,       // Соответствует CSRF_COOKIE_SECURE = True
            httpOnly: true,     // Соответствует CSRF_COOKIE_HTTPONLY = True
            sameSite: 'Lax',    // Соответствует CSRF_COOKIE_SAMESITE = 'Lax'
            maxAge: 24 * 60 * 60 * 1000,
            path: '/',
            domain: cookieDomain
        });

        next();
    } catch (error) {
        console.error('Cookie error:', error);
        next(error);
    }
});

// Middleware для генерации nonce и добавления CSP-заголовка
app.use((req, res, next) => {
    try {
        const nonce = crypto.randomBytes(16).toString("base64");
        res.locals.nonce = nonce;
        res.setHeader(
            "Content-Security-Policy",
            `default-src 'self'; script-src 'self' 'nonce-${nonce}' https://cdn.jsdelivr.net; style-src 'self' 'nonce-${nonce}' https://cdn.jsdelivr.net; img-src 'self' data:`
        );
        next();
    } catch (error) {
        console.error('CSP error:', error);
        next(error);
    }
});

// Обработка ошибок
app.use((err, req, res, next) => {
    console.error('Server error:', err);
    res.status(err.status || 500).json({
        error: {
            message: err.message || 'Internal Server Error',
            status: err.status || 500
        }
    });
});

// Пример API маршрута с обработкой ошибок
app.post("/api/register", (req, res, next) => {
    try {
        const {username, email, password} = req.body;
        if (!username || !email || !password) {
            return res.status(400).json({
                error: {
                    message: 'Missing required fields',
                    status: 400
                }
            });
        }
        console.log("Данные регистрации:", {username, email, password});
        res.json({message: "User registered successfully"});
    } catch (error) {
        next(error);
    }
});

// Обработчик отчетов о нарушениях CSP
app.post("/csp-violation-report-endpoint", (req, res) => {
    console.log("CSP Violation:", req.body);
    res.status(204).end();
});

// Маршрут для рендеринга главной страницы
app.get("/", (req, res, next) => {
    try {
        res.sendFile(path.join(__dirname, "public", "index.html"));
    } catch (error) {
        next(error);
    }
});

// Обработка несуществующих маршрутов
app.use((req, res) => {
    res.status(404).json({
        error: {
            message: 'Not Found',
            status: 404
        }
    });
});

// Добавление сервера с обработкой ошибок
const server = app.listen(port, () => {
    console.log(`Сервер запущен на порту ${port}`);
}).on('error', (error) => {
    console.error('Server error:', error);
    if (error.code === 'EADDRINUSE') {
        console.error(`Порт ${port} уже используется`);
    }
});

// Graceful shutdown
process.on('SIGTERM', () => {
    console.log('SIGTERM получен. Закрытие сервера...');
    server.close(() => {
        console.log('Сервер закрыт');
        process.exit(0);
    });
});