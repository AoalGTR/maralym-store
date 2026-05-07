# 🚀 Гайд по деплою MaralYm на Render + Vercel

Этот гайд поможет выложить сайт в интернет за 15 минут.

---

## 📋 Что нужно:
1. Аккаунт на [Render.com](https://render.com) (free)
2. Аккаунт на [Vercel.com](https://vercel.com) (free)
3. GitHub репозиторий с этим проектом (git push)

---

## 🔧 Шаг 1: Подготовка (локально, на твоём ПК)

### 1.1 Инициализируй git репозиторий
```bash
cd /Users/marselmannapov/Desktop/collegepj/calculator
git init
git add .
git commit -m "Initial commit: MaralYm e-commerce"
```

### 1.2 Создай репозиторий на GitHub
- Перейди на [github.com/new](https://github.com/new)
- Создай репозиторий `maralym-store` (приватный или публичный)
- Скопируй SSH URL из кнопки "Code"

### 1.3 Привяжи remote и загрузи код
```bash
git remote add origin git@github.com:YOUR_USERNAME/maralym-store.git
git branch -M main
git push -u origin main
```

---

## 🚀 Шаг 2: Деплой Backend на Render

### 2.1 Зайди на [Render.com](https://render.com)
- Кликни "+ New" → "Web Service"
- Выбери свой GitHub репозиторий `maralym-store`

### 2.2 Настрой параметры:
| Параметр | Значение |
|----------|----------|
| **Name** | maralym-api |
| **Environment** | Python 3 |
| **Build Command** | `pip install -r backend/requirements.txt` |
| **Start Command** | `gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:$PORT backend.main:app` |
| **Plan** | Free |

### 2.3 Нажми "Create Web Service"
- Ждёшь ~2 минуты пока Render разворачивает приложение
- Копируешь URL вида `https://maralym-api.onrender.com`

**Сохрани этот URL — он нужен для фронтенда!**

---

## 🌐 Шаг 3: Обновление Frontend для Production

### 3.1 Обнови API_BASE в `vizitka/script.js`

Открой файл и найди строку:
```javascript
const API_BASE = 'http://localhost:8000/api';
```

Замени на (подставь свой URL с Render):
```javascript
const API_BASE = 'https://maralym-api.onrender.com/api';
// или просто:
const API_BASE = 'https://YOUR-RENDER-URL/api';
```

### 3.2 Загрузи обновление в GitHub
```bash
git add vizitka/script.js
git commit -m "Update API_BASE for production"
git push
```

---

## 🎨 Шаг 4: Деплой Frontend на Vercel

### 4.1 Зайди на [Vercel.com](https://vercel.com)
- Кликни "Add New..." → "Project"
- Импортируй свой GitHub репозиторий `maralym-store`

### 4.2 Настрой деплой:
| Параметр | Значение |
|----------|----------|
| **Framework Preset** | Other |
| **Root Directory** | vizitka |
| **Build Command** | (оставь пустым) |
| **Output Directory** | (оставь пустым) |

### 4.3 Нажми "Deploy"
- Ждёшь ~1 минуту
- Копируешь URL вида `https://maralym-store.vercel.app`

---

## ✅ Готово!

Твой сайт теперь доступен по адресу:
```
https://маралим.vercel.app
```

**Проверь:**
1. Открой сайт в браузере
2. Добавь товар в корзину
3. Попробуй войти (login) и оформить заказ

Если видишь ошибки типа "Cannot load products":
- Проверь, что URL Render в `vizitka/script.js` правильный
- Зайди на Render даш и проверь логи (Logs tab)

---

## 🔄 Как обновить сайт после изменений

```bash
# Сделай изменения локально
# ...

# Загрузи на GitHub
git add .
git commit -m "Fix: описание изменений"
git push

# Render и Vercel автоматически перезагрузят приложения (~1-2 минуты)
```

---

## 🐛 Если что-то не работает

### Backend не грузит данные
- Проверь URL в `vizitka/script.js`
- Открой консоль браузера (F12 → Console) и посмотри ошибки
- Зайди на Render → твоё приложение → "Logs"

### CORS ошибка (blocked by CORS policy)
- Убедись что в `backend/main.py` стоит CORS middleware с `allow_origins=["*"]`

### Фронтенд не загружается
- Проверь что files находятся в папке `vizitka/` (index.html, script.js, style.css)

---

## 📊 Мониторинг

- **Render**: https://dashboard.render.com → твоё приложение → Logs
- **Vercel**: https://vercel.com/dashboard → твой проект → Deployments

---

**Успехов! 🎉**
