# 🔐 JWT/Cookies Multi-User Implementation Plan

Этот гайд для добавления настоящей безопасной авторизации с JWT и signed cookies.

---

## 🎯 Цель

Сейчас: один пользователь, одна сессия в `state.json`
После: каждый браузер получает signed cookie, может одновременно использоваться много юзеров

---

## 📊 Архитектура изменений

### Backend changes (backend/main.py)
1. Добавить `python-jose` + `passlib` для JWT
2. Создать функцию `create_access_token(email)` → JWT токен
3. Обновить `/api/login` → возвращать set-cookie header
4. Добавить middleware для проверки cookie в каждом запросе
5. Изменить `load_state()` → брать email из cookie вместо глобального

### Frontend changes (vizitka/script.js)
1. Обновить `handleLogin()` → браузер автоматически сохранит cookie
2. Обновить `initState()` → не передавать email в запросе (браузер пошлёт cookie автоматически)
3. Обновить `handleLogout()` → очистить cookie

---

## 📦 Зависимости (backend/requirements.txt)

```
python-jose[cryptography]>=3.3
passlib[bcrypt]>=1.7
python-multipart>=0.0.5
```

---

## 🔑 Основные изменения кода

### 1. backend/main.py — JWT конфиг и функции

```python
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

# Секретный ключ (должен быть в переменной окружения!)
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 30

def create_access_token(email: str):
    """Create JWT token for email"""
    expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    payload = {"sub": email, "exp": expire}
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_email_from_token(token: str) -> str:
    """Extract email from JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        return email
    except JWTError:
        return None
```

### 2. backend/main.py — обновить /api/login

```python
@app.post("/api/login")
def login(payload: LoginIn, response: Response):
    email = str(payload.email)
    
    # Create JWT token
    token = create_access_token(email)
    
    # Set as secure HTTP-only cookie
    response.set_cookie(
        key="auth_token",
        value=token,
        httponly=True,
        secure=True,  # HTTPS only in production
        samesite="lax",
        max_age=30*24*60*60  # 30 days
    )
    
    # Also update state.json
    state = load_state()
    state["session_email"] = email
    save_state(state)
    
    return {
        "email": email,
        "user_profile": state.get("user_profile", {})
    }
```

### 3. backend/main.py — Dependency для проверки авторизации

```python
from fastapi import Depends, HTTPException

def get_current_email(request: Request) -> str:
    """Extract email from cookie"""
    token = request.cookies.get("auth_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    email = get_email_from_token(token)
    if not email:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return email
```

### 4. backend/main.py — Пример защищенного endpoint

```python
@app.get("/api/profile")
def get_profile(email: str = Depends(get_current_email)):
    """Get current user's profile (only if logged in)"""
    state = load_state()
    return {"user_profile": state.get("user_profile", {})}
```

---

## 🌐 Frontend изменения

### vizitka/script.js — обновить initState

```javascript
async function initState() {
  try {
    // Браузер автоматически шлёт cookies в запросе
    const stateRes = await fetch(`${API_BASE}/state`, {
      credentials: 'include'  // Это важно!
    });
    
    if (stateRes.ok) {
      const data = await stateRes.json();
      cart = data.cart || [];
      favorites = data.favorites || [];
      orders = data.orders || [];
      userProfile = data.user_profile || userProfile;
      
      // session_email больше не нужен — он в cookie
    }
  } catch (err) {
    console.warn('Failed to load state', err);
  }
}
```

### vizitka/script.js — обновить handleLogin

```javascript
async function handleLogin(email) {
  try {
    const res = await fetch(`${API_BASE}/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email }),
      credentials: 'include'  // Важно: принять cookie
    });
    
    if (res.ok) {
      // Cookie уже установлена браузером!
      document.getElementById('loginModal').classList.remove('open');
      window.location.reload();  // Перезагрузить страницу
      return true;
    }
  } catch (err) {
    console.warn('Login failed:', err);
  }
  return false;
}
```

---

## ✅ Тестирование JWT

```bash
# Unit test с JWT
python backend/tests/test_jwt_auth.py
```

---

## 🚀 Миграция на production

1. Установить переменную окружения `SECRET_KEY` на Render
   - Render dashboard → Settings → Environment Variables
   - Генерируй 256-bit string: `openssl rand -hex 32`

2. Включить HTTPS (Render делает автоматически)

3. Пересчитать cookie флаги (secure=True для HTTPS)

---

## 🔄 Timeline

- ⏱️ **2–3 часа** на реализацию с тестами
- ⏱️ **30 минут** на отладку CORS + cookies
- ⏱️ **15 минут** на деплой

---

## ❓ FAQ

**Q: Нужно ли удалять localStorage?**
A: Нет, можешь оставить как fallback

**Q: Сломается ли после деплоя?**
A: Может, если забудешь установить SECRET_KEY на Render

**Q: Можно ли использовать обычный token вместо cookie?**
A: Да, но cookie безопаснее (защита от XSS)

---

**Следующий шаг:** Начни с установки зависимостей, потом обновляй backend/main.py по плану выше.
