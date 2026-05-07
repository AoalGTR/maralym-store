# MaralYm — Женская одежда премиум-класса

Полнофункциональный e-commerce магазин с фронтенд (HTML/CSS/JS) и backend API (FastAPI).

## 🎯 Функции

- **Каталог товаров** — поиск, фильтры по категории и цене
- **Корзина** — добавление/удаление товаров
- **Избранное** — сохранение любимых товаров
- **Авторизация** — вход по email
- **Профиль** — сохранение данных и история заказов
- **Оформление заказа** — checkout с выбором доставки

## 📂 Структура проекта

```
calculator/
├── vizitka/                 # Frontend (HTML/CSS/JS)
│   ├── index.html
│   ├── style.css
│   └── script.js
├── backend/                 # API (FastAPI)
│   ├── main.py              # Application main
│   ├── state.json           # Data storage (JSON)
│   ├── requirements.txt      # Python dependencies
│   └── tests/
│       ├── run_auth_tests.py      # Auth smoke tests
│       └── test_endpoints.py      # Full endpoint tests (17 tests)
├── Procfile                 # Render deployment
├── vercel.json              # Vercel config
└── DEPLOY_GUIDE.md          # Deployment instructions
```

## 🚀 Быстрый старт (локально)

### Backend

```bash
cd calculator
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload
```

Backend будет доступен на `http://localhost:8000`

### Frontend

```bash
cd vizitka
python -m http.server 8001
```

Frontend будет доступен на `http://localhost:8001`

### Тесты

```bash
# Auth tests
python backend/tests/run_auth_tests.py

# Full endpoint tests (17 tests)
python backend/tests/test_endpoints.py
```

## 📦 Технологический стек

### Frontend
- HTML5
- CSS3 (Flexbox, Grid)
- Vanilla JavaScript (ES6)
- Google Fonts (Manrope, Bebas Neue)

### Backend
- Python 3.12
- FastAPI
- Uvicorn ASGI
- Pydantic (validation)
- JSON file storage

## 🌐 Деплой

**[Полные инструкции деплоя →](DEPLOY_GUIDE.md)**

Быстро:
1. Инициализируй git и загрузи на GitHub
2. Деплой backend на Render.com (free tier)
3. Обнови API_BASE в `vizitka/script.js`
4. Деплой frontend на Vercel.com (free tier)

## 🧪 Тестирование

Проект включает:
- ✅ 2 smoke test для авторизации
- ✅ 17 unit tests для всех endpoint'ов
- ✅ CORS middleware для cross-origin запросов
- ✅ Graceful fallback to localStorage

## 📋 API Endpoints

| Метод | Endpoint | Описание |
|-------|----------|---------|
| GET | `/api/health` | Health check |
| GET | `/api/products` | Список товаров |
| GET | `/api/products/{id}` | Один товар |
| GET/PUT | `/api/cart` | Корзина |
| POST | `/api/login` | Вход |
| POST | `/api/logout` | Выход |
| GET/POST | `/api/favorites` | Избранное |
| PUT | `/api/profile` | Профиль |
| POST | `/api/checkout` | Оформление заказа |
| GET | `/api/orders` | История заказов |

## 🔐 Безопасность

- CORS включен для `http://localhost:8001` (dev) и production URL
- Email валидация через Pydantic
- Базовая сессия через `session_email` в JSON
- *(Планируется: JWT/signed cookies для multi-user)*

## 📝 Лицензия

MIT

## 👤 Автор

MaralYm Development Team

---

**Начни с деплоя:** [DEPLOY_GUIDE.md](DEPLOY_GUIDE.md)
