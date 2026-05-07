from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field


BASE_DIR = Path(__file__).resolve().parent
STATE_FILE = BASE_DIR / "state.json"


PRODUCTS = [
    {
        "id": 1,
        "name": "Белая женская рубашка Classic Fit",
        "category": "shirts",
        "badge": "Рубашка",
        "image": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?auto=format&fit=crop&w=1000&q=80",
        "price": 2490,
        "description": "Лёгкая женская рубашка из хлопка для офиса и повседневных образов.",
        "tags": ["XS", "S", "M", "L"],
        "rating": 4.5,
    },
    {
        "id": 2,
        "name": "Голубая женская рубашка Linen Line",
        "category": "shirts",
        "badge": "Рубашка",
        "image": "https://images.unsplash.com/photo-1485462537746-965f33f7f6a7?auto=format&fit=crop&w=1000&q=80",
        "price": 2790,
        "description": "Воздушная рубашка с мягкой посадкой и аккуратным воротником.",
        "tags": ["S", "M", "L", "XL"],
        "rating": 4.8,
    },
    {
        "id": 3,
        "name": "Чёрные женские брюки Urban Slim",
        "category": "pants",
        "badge": "Брюки",
        "image": "https://images.unsplash.com/photo-1475180098004-ca77a66827be?auto=format&fit=crop&w=1000&q=80",
        "price": 3190,
        "description": "Строгие брюки для современного и чистого силуэта.",
        "tags": ["40", "42", "44", "46"],
        "rating": 4.3,
    },
    {
        "id": 4,
        "name": "Светлые женские джинсы Relaxed",
        "category": "pants",
        "badge": "Брюки",
        "image": "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?auto=format&fit=crop&w=1000&q=80",
        "price": 2990,
        "description": "Комфортные джинсы с универсальной посадкой на каждый день.",
        "tags": ["40", "42", "44", "46"],
        "rating": 4.6,
    },
    {
        "id": 5,
        "name": "Чёрное женское платье Evening Mood",
        "category": "dresses",
        "badge": "Платье",
        "image": "https://images.unsplash.com/photo-1496747611176-843222e1e57c?auto=format&fit=crop&w=1000&q=80",
        "price": 4590,
        "description": "Элегантное вечернее платье для особых случаев и мероприятий.",
        "tags": ["XS", "S", "M", "L"],
        "rating": 4.9,
    },
    {
        "id": 6,
        "name": "Платье Rose Satin",
        "category": "dresses",
        "badge": "Платье",
        "image": "https://images.unsplash.com/photo-1524504388940-b1c1722653e1?auto=format&fit=crop&w=1000&q=80",
        "price": 3890,
        "description": "Мягкий сатиновый блеск и плавный силуэт для яркого выхода.",
        "tags": ["XS", "S", "M", "L"],
        "rating": 4.7,
    },
    {
        "id": 7,
        "name": "Кожаная женская куртка Black Edge",
        "category": "outerwear",
        "badge": "Куртка",
        "image": "https://images.unsplash.com/photo-1529139574466-a303027c1d8b?auto=format&fit=crop&w=1000&q=80",
        "price": 7990,
        "description": "Смелая базовая куртка, которая собирает образ и добавляет характер.",
        "tags": ["S", "M", "L", "XL"],
        "rating": 4.4,
    },
    {
        "id": 8,
        "name": "Бежевая женская куртка Soft Warm",
        "category": "outerwear",
        "badge": "Куртка",
        "image": "https://images.unsplash.com/photo-1483985988355-763728e1935b?auto=format&fit=crop&w=1000&q=80",
        "price": 6990,
        "description": "Утеплённая модель для прохладной погоды и спокойных образов.",
        "tags": ["S", "M", "L", "XL"],
        "rating": 4.5,
    },
    {
        "id": 9,
        "name": "Рубашка Stripe Office",
        "category": "shirts",
        "badge": "Рубашка",
        "image": "https://images.unsplash.com/photo-1434389677669-e08b4cac3105?auto=format&fit=crop&w=1000&q=80",
        "price": 2290,
        "description": "Полосатая женская рубашка с деловым характером и лёгким акцентом.",
        "tags": ["XS", "S", "M", "L"],
        "rating": 4.2,
    },
    {
        "id": 10,
        "name": "Женские брюки Wide Comfort",
        "category": "pants",
        "badge": "Брюки",
        "image": "https://images.unsplash.com/photo-1445205170230-053b83016050?auto=format&fit=crop&w=1000&q=80",
        "price": 3390,
        "description": "Широкий крой и удобная посадка для современного гардероба.",
        "tags": ["40", "42", "44", "46"],
        "rating": 4.7,
    },
    {
        "id": 11,
        "name": "Платье Day Light",
        "category": "dresses",
        "badge": "Платье",
        "image": "https://images.unsplash.com/photo-1464863979621-258859e62245?auto=format&fit=crop&w=1000&q=80",
        "price": 3690,
        "description": "Лаконичное платье на каждый день с мягким и женственным силуэтом.",
        "tags": ["XS", "S", "M", "L"],
        "rating": 4.6,
    },
    {
        "id": 12,
        "name": "Джинсовая женская куртка Blue Denim",
        "category": "outerwear",
        "badge": "Куртка",
        "image": "https://images.unsplash.com/photo-1441986300917-64674bd600d8?auto=format&fit=crop&w=1000&q=80",
        "price": 4190,
        "description": "Классическая джинсовая куртка, которая не выходит из моды.",
        "tags": ["S", "M", "L", "XL"],
        "rating": 4.8,
    },
]


DEFAULT_STATE = {
    "cart": [],
    "favorites": [],
    "orders": [],
    "session_email": "",
    "user_profile": {"name": "", "email": "", "phone": "", "address": ""},
}


def load_state() -> dict[str, Any]:
    if not STATE_FILE.exists():
        return DEFAULT_STATE.copy()

    with STATE_FILE.open("r", encoding="utf-8") as file_handle:
        data = json.load(file_handle)

    state = DEFAULT_STATE.copy()
    state.update(data)
    return state


def save_state(state: dict[str, Any]) -> None:
    with STATE_FILE.open("w", encoding="utf-8") as file_handle:
        json.dump(state, file_handle, ensure_ascii=False, indent=2)


def get_product(product_id: int) -> dict[str, Any]:
    product = next((item for item in PRODUCTS if item["id"] == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


class CartItemIn(BaseModel):
    id: int
    quantity: int = Field(ge=1)
    size: str | None = None


class FavoritesIn(BaseModel):
    product_id: int


class ProfileIn(BaseModel):
    name: str = ""
    email: EmailStr | str = ""
    phone: str = ""
    address: str = ""


class LoginIn(BaseModel):
    email: EmailStr | str



class CheckoutIn(BaseModel):
    name: str
    email: EmailStr | str
    phone: str
    address: str
    delivery: Literal["pickup", "delivery", "express"] = "delivery"
    items: list[CartItemIn]


app = FastAPI(title="MaralYm API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/login")
def login(payload: LoginIn) -> dict[str, Any]:
    state = load_state()
    state["session_email"] = str(payload.email)
    save_state(state)
    return {"session_email": state["session_email"], "user_profile": state["user_profile"]}


@app.post("/api/logout")
def logout() -> dict[str, str]:
    state = load_state()
    state["session_email"] = ""
    save_state(state)
    return {"message": "Logged out successfully"}


@app.get("/api/products")
def list_products(category: str | None = None, q: str | None = None, max_price: int | None = None) -> dict[str, Any]:
    items = PRODUCTS

    if category and category != "all":
        items = [product for product in items if product["category"] == category]

    if max_price is not None:
        items = [product for product in items if product["price"] <= max_price]

    if q:
        query = q.lower().strip()
        items = [
            product
            for product in items
            if query in product["name"].lower() or query in product["description"].lower()
        ]

    return {"items": items, "count": len(items)}


@app.get("/api/products/{product_id}")
def read_product(product_id: int) -> dict[str, Any]:
    return get_product(product_id)


@app.get("/api/state")
def read_state() -> dict[str, Any]:
    return load_state()


@app.put("/api/profile")
def update_profile(profile: ProfileIn) -> dict[str, Any]:
    state = load_state()
    state["user_profile"] = profile.model_dump()
    save_state(state)
    return {"user_profile": state["user_profile"]}


@app.get("/api/cart")
def read_cart() -> dict[str, Any]:
    return {"cart": load_state()["cart"]}


@app.put("/api/cart")
def replace_cart(items: list[CartItemIn]) -> dict[str, Any]:
    state = load_state()
    normalized_cart = []

    for item in items:
        product = get_product(item.id)
        normalized_cart.append(
            {
                "id": item.id,
                "name": product["name"],
                "price": product["price"],
                "quantity": item.quantity,
                "size": item.size,
            }
        )

    state["cart"] = normalized_cart
    save_state(state)
    return {"cart": state["cart"]}


@app.get("/api/favorites")
def read_favorites() -> dict[str, Any]:
    return {"favorites": load_state()["favorites"]}


@app.post("/api/favorites/toggle")
def toggle_favorite(payload: FavoritesIn) -> dict[str, Any]:
    state = load_state()
    product = get_product(payload.product_id)

    favorites = state["favorites"]
    if payload.product_id in favorites:
        favorites.remove(payload.product_id)
        favorite = False
    else:
        favorites.append(payload.product_id)
        favorite = True

    state["favorites"] = favorites
    save_state(state)
    return {"favorite": favorite, "product": product, "favorites": favorites}


@app.get("/api/orders")
def list_orders() -> dict[str, Any]:
    return {"orders": load_state()["orders"]}


@app.post("/api/checkout")
def checkout(payload: CheckoutIn) -> dict[str, Any]:
    state = load_state()

    subtotal = 0
    normalized_items = []

    for item in payload.items:
        product = get_product(item.id)
        line_total = product["price"] * item.quantity
        subtotal += line_total
        normalized_items.append(
            {
                "id": product["id"],
                "name": product["name"],
                "price": product["price"],
                "quantity": item.quantity,
                "size": item.size,
                "line_total": line_total,
            }
        )

    delivery_fee = 0 if payload.delivery == "pickup" else 500 if payload.delivery == "delivery" else 1500
    total = subtotal + delivery_fee
    order_id = int(datetime.now(tz=timezone.utc).timestamp())

    order = {
        "id": order_id,
        "date": datetime.now(tz=timezone.utc).isoformat(),
        "items": sum(item.quantity for item in payload.items),
        "subtotal": subtotal,
        "delivery_fee": delivery_fee,
        "total": total,
        "delivery": payload.delivery,
        "customer": {
            "name": payload.name,
            "email": str(payload.email),
            "phone": payload.phone,
            "address": payload.address,
        },
        "products": normalized_items,
    }

    state["user_profile"] = {
        "name": payload.name,
        "email": str(payload.email),
        "phone": payload.phone,
        "address": payload.address,
    }
    state["orders"].append(order)
    state["cart"] = []
    save_state(state)

    return {"order": order, "user_profile": state["user_profile"], "cart": []}
