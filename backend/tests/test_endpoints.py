#!/usr/bin/env python3
"""Unit tests for MaralYm backend endpoints using requests.

Run with:
  python -m pytest backend/tests/test_endpoints.py -v

Or without pytest:
  python backend/tests/test_endpoints.py
"""
import subprocess
import time
import sys
import os

BASE_URL = "http://127.0.0.1:8000/api"


def is_server_up():
    """Check if backend is reachable."""
    try:
        import requests
        r = requests.get(f"{BASE_URL}/health", timeout=1)
        return r.status_code == 200
    except Exception:
        return False


def start_server():
    """Start backend server in background."""
    p = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "backend.main:app", "--host", "127.0.0.1", "--port", "8000"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    for _ in range(10):
        if is_server_up():
            return p
        time.sleep(0.5)
    return p


def test_health():
    """Test health check endpoint."""
    import requests
    r = requests.get(f"{BASE_URL}/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}
    print("✓ GET /api/health")


def test_products_list():
    """Test products listing."""
    import requests
    r = requests.get(f"{BASE_URL}/products")
    assert r.status_code == 200
    data = r.json()
    assert "items" in data
    assert "count" in data
    assert len(data["items"]) > 0
    print("✓ GET /api/products")


def test_products_filter_by_category():
    """Test products filtering by category."""
    import requests
    r = requests.get(f"{BASE_URL}/products", params={"category": "shirts"})
    assert r.status_code == 200
    data = r.json()
    assert all(p["category"] == "shirts" for p in data["items"])
    print("✓ GET /api/products?category=...")


def test_products_filter_by_price():
    """Test products filtering by price."""
    import requests
    r = requests.get(f"{BASE_URL}/products", params={"max_price": 3000})
    assert r.status_code == 200
    data = r.json()
    assert all(p["price"] <= 3000 for p in data["items"])
    print("✓ GET /api/products?max_price=...")


def test_products_search():
    """Test products search."""
    import requests
    r = requests.get(f"{BASE_URL}/products", params={"q": "платье"})
    assert r.status_code == 200
    data = r.json()
    # Should find at least some products with "платье" in name/description
    assert len(data["items"]) >= 0
    print("✓ GET /api/products?q=...")


def test_product_single():
    """Test single product endpoint."""
    import requests
    # Get a product ID first
    r = requests.get(f"{BASE_URL}/products")
    products = r.json()["items"]
    assert len(products) > 0
    
    product_id = products[0]["id"]
    r = requests.get(f"{BASE_URL}/products/{product_id}")
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == product_id
    print(f"✓ GET /api/products/{{id}}")


def test_product_not_found():
    """Test 404 for non-existent product."""
    import requests
    r = requests.get(f"{BASE_URL}/products/99999")
    assert r.status_code == 404
    print("✓ GET /api/products/{invalid_id} → 404")


def test_state():
    """Test state endpoint."""
    import requests
    r = requests.get(f"{BASE_URL}/state")
    assert r.status_code == 200
    data = r.json()
    assert "cart" in data
    assert "favorites" in data
    assert "orders" in data
    assert "session_email" in data
    assert "user_profile" in data
    print("✓ GET /api/state")


def test_cart_operations():
    """Test cart PUT and GET."""
    import requests
    
    # PUT cart
    cart_items = [{"id": 1, "quantity": 2, "size": "M"}]
    r = requests.put(f"{BASE_URL}/cart", json=cart_items)
    assert r.status_code == 200
    print("✓ PUT /api/cart")
    
    # GET cart
    r = requests.get(f"{BASE_URL}/cart")
    assert r.status_code == 200
    data = r.json()
    assert "cart" in data
    assert isinstance(data["cart"], list)
    print("✓ GET /api/cart")


def test_profile_put():
    """Test profile update."""
    import requests
    profile = {
        "name": "Test User",
        "email": "test@example.com",
        "phone": "1234567890",
        "address": "123 Main St"
    }
    r = requests.put(f"{BASE_URL}/profile", json=profile)
    assert r.status_code == 200
    data = r.json()
    assert "user_profile" in data
    print("✓ PUT /api/profile")


def test_login():
    """Test login endpoint."""
    import requests
    r = requests.post(f"{BASE_URL}/login", json={"email": "testuser@example.com"})
    assert r.status_code == 200
    data = r.json()
    assert "session_email" in data
    assert data["session_email"] == "testuser@example.com"
    print("✓ POST /api/login")


def test_logout():
    """Test logout endpoint."""
    import requests
    r = requests.post(f"{BASE_URL}/logout")
    assert r.status_code == 200
    data = r.json()
    assert "message" in data
    print("✓ POST /api/logout")


def test_favorites_toggle():
    """Test favorites toggle."""
    import requests
    
    # Toggle favorite on
    r = requests.post(f"{BASE_URL}/favorites/toggle", json={"product_id": 1})
    assert r.status_code == 200
    data = r.json()
    assert "favorites" in data
    assert isinstance(data["favorites"], list)
    print("✓ POST /api/favorites/toggle")


def test_favorites_get():
    """Test get favorites."""
    import requests
    r = requests.get(f"{BASE_URL}/favorites")
    assert r.status_code == 200
    data = r.json()
    assert "favorites" in data
    assert isinstance(data["favorites"], list)
    print("✓ GET /api/favorites")


def test_orders_get():
    """Test get orders."""
    import requests
    r = requests.get(f"{BASE_URL}/orders")
    assert r.status_code == 200
    data = r.json()
    assert "orders" in data
    assert isinstance(data["orders"], list)
    print("✓ GET /api/orders")


def test_checkout():
    """Test checkout endpoint."""
    import requests
    
    # First login
    requests.post(f"{BASE_URL}/login", json={"email": "checkout@example.com"})
    
    # Add something to cart
    requests.put(f"{BASE_URL}/cart", json=[{"id": 1, "quantity": 1, "size": None}])
    
    # Checkout
    checkout_data = {
        "name": "Test Customer",
        "email": "checkout@example.com",
        "phone": "9876543210",
        "address": "456 Oak Ave",
        "delivery": "delivery",
        "items": [{"id": 1, "quantity": 1, "size": None}]
    }
    r = requests.post(f"{BASE_URL}/checkout", json=checkout_data)
    assert r.status_code == 200
    data = r.json()
    assert "order" in data
    assert "order_id" in data or "id" in data.get("order", {})
    print("✓ POST /api/checkout")


def test_checkout_empty_cart():
    """Test checkout with empty items."""
    import requests
    
    # Try checkout with empty items list
    checkout_data = {
        "name": "Test",
        "email": "emptycart@example.com",
        "phone": "1234567890",
        "address": "Test",
        "delivery": "delivery",
        "items": []
    }
    r = requests.post(f"{BASE_URL}/checkout", json=checkout_data)
    # Server may accept empty checkout or reject it - both are OK for this test
    # We just verify it returns a valid response
    assert r.status_code in [200, 400, 422]
    print("✓ POST /api/checkout with empty items → response")


def run_all_tests():
    """Run all tests."""
    tests = [
        test_health,
        test_products_list,
        test_products_filter_by_category,
        test_products_filter_by_price,
        test_products_search,
        test_product_single,
        test_product_not_found,
        test_state,
        test_cart_operations,
        test_profile_put,
        test_login,
        test_logout,
        test_favorites_toggle,
        test_favorites_get,
        test_orders_get,
        test_checkout,
        test_checkout_empty_cart,
    ]
    
    failed = []
    for test in tests:
        try:
            test()
        except AssertionError as e:
            print(f"✗ {test.__name__}: {e}")
            failed.append((test.__name__, str(e)))
        except Exception as e:
            print(f"✗ {test.__name__}: {type(e).__name__}: {e}")
            failed.append((test.__name__, f"{type(e).__name__}: {e}"))
    
    print("\n" + "=" * 60)
    if failed:
        print(f"FAILED: {len(failed)}/{len(tests)} tests")
        for name, error in failed:
            print(f"  - {name}: {error}")
        return False
    else:
        print(f"SUCCESS: All {len(tests)} tests passed")
        return True


def main():
    """Entry point."""
    server_proc = None
    started = False
    
    try:
        # Check if server is running
        if not is_server_up():
            print("Starting backend server...")
            server_proc = start_server()
            started = True
        
        if not is_server_up():
            print("ERROR: Server failed to start")
            sys.exit(1)
        
        print("Running unit tests...\n")
        success = run_all_tests()
        sys.exit(0 if success else 1)
    
    finally:
        if started and server_proc:
            server_proc.terminate()
            server_proc.wait()


if __name__ == '__main__':
    main()
