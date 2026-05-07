# MaralYm backend

FastAPI backend for the MaralYm storefront.

## Run

```bash
cd /Users/marselmannapov/Desktop/collegepj/calculator
source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload
```

## API

- `GET /api/health`
- `GET /api/products`
- `GET /api/products/{product_id}`
- `GET /api/state`
- `PUT /api/profile`
- `GET /api/cart`
- `PUT /api/cart`
- `GET /api/favorites`
- `POST /api/favorites/toggle`
- `GET /api/orders`
- `POST /api/checkout`
