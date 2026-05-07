#!/usr/bin/env python3
"""Simple smoke test for login/logout endpoints.

Usage:
  python backend/tests/run_auth_tests.py

The script will try to hit http://127.0.0.1:8000; if unreachable, it will attempt
to start a local uvicorn process and then run the checks.
"""
import subprocess
import time
import requests
import sys

BASE = "http://127.0.0.1:8000"


def is_up():
    try:
        r = requests.get(f"{BASE}/api/health", timeout=1)
        return r.status_code == 200
    except Exception:
        return False


def start_server():
    # Start uvicorn in background
    p = subprocess.Popen([
        sys.executable, "-m", "uvicorn", "backend.main:app", "--host", "127.0.0.1", "--port", "8000"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # wait a bit
    for _ in range(10):
        if is_up():
            return p
        time.sleep(0.5)
    return p


def run_tests():
    print('Checking /api/login...')
    r1 = requests.post(f"{BASE}/api/login", json={"email": "test-run@example.com"}, timeout=5)
    assert r1.status_code == 200, f"login failed: {r1.status_code}"
    j = r1.json()
    assert 'session_email' in j, f"unexpected login response: {j}"
    print(' login OK ->', j.get('session_email'))

    print('Checking /api/logout...')
    r2 = requests.post(f"{BASE}/api/logout", timeout=5)
    assert r2.status_code == 200, f"logout failed: {r2.status_code}"
    print(' logout OK')


def main():
    server_proc = None
    started = False
    try:
        if not is_up():
            print('Server not reachable — starting uvicorn...')
            server_proc = start_server()
            started = True

        if not is_up():
            print('Server still not reachable. Aborting.', file=sys.stderr)
            sys.exit(2)

        run_tests()
        print('All tests passed.')
    except AssertionError as e:
        print('TEST FAILED:', e, file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print('ERROR:', e, file=sys.stderr)
        sys.exit(3)
    finally:
        if started and server_proc:
            server_proc.terminate()


if __name__ == '__main__':
    main()
