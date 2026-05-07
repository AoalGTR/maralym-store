"""
Примеры использования User Management System
"""
import datetime
from user_management import User, UserService, UserUtil

# ========== ПРИМЕР 1: Создание пользователей ==========
print("=" * 60)
print("ПРИМЕР 1: Создание пользователей")
print("=" * 60)

# Создаем пользователя
user1 = User(
    user_id=240000001,
    name="Иван",
    surname="Петров",
    birthday=datetime.datetime(2000, 5, 15)
)

# Задаем email и пароль
user1.email = "ivan.petrov@mail.com"
user1.password = "SecurePass123!"

print(f"\n✓ Пользователь создан: {user1.name} {user1.surname}")
print(f"  Email: {user1.email}")
print(f"  ID: {user1.user_id}")
print(f"  Возраст: {user1.get_age()} лет")


# ========== ПРИМЕР 2: Использование утилит ==========
print("\n" + "=" * 60)
print("ПРИМЕР 2: Использование утилит UserUtil")
print("=" * 60)

# Генерируем уникальный ID
new_id = UserUtil.generate_user_id()
print(f"\n✓ Сгенерирован ID: {new_id}")

# Генерируем пароль
new_password = UserUtil.generate_password()
print(f"✓ Сгенерирован пароль: {new_password}")
print(f"  Пароль надежный? {UserUtil.is_strong_password(new_password)}")

# Генерируем email
email = UserUtil.generate_email("Мария", "Сидорова", "company.com")
print(f"✓ Сгенерирован email: {email}")

# Проверяем email
is_valid = UserUtil.validate_email(email)
print(f"  Email валидный? {is_valid}")


# ========== ПРИМЕР 3: Проверка паролей ==========
print("\n" + "=" * 60)
print("ПРИМЕР 3: Проверка надежности паролей")
print("=" * 60)

test_passwords = [
    ("Pass123!", "СЛАБЫЙ - слишком короткий"),
    ("password123", "СЛАБЫЙ - нет заглавных букв и спецсимволов"),
    ("Password123!", "НАДЕЖНЫЙ"),
    ("MySecure@Pass2024", "НАДЕЖНЫЙ"),
]

for password, description in test_passwords:
    is_strong = UserUtil.is_strong_password(password)
    icon = "✓" if is_strong else "✗"
    print(f"{icon} '{password}' - {description}")


# ========== ПРИМЕР 4: Проверка emails ==========
print("\n" + "=" * 60)
print("ПРИМЕР 4: Проверка valid emails")
print("=" * 60)

test_emails = [
    ("ivan.petrov@mail.com", True),
    ("maria.sidorova@company.org", True),
    ("invalidemailcom", False),
    ("ivan@petrov@mail.com", False),
    ("ivan.petrov", False),
]

for email, should_be_valid in test_emails:
    is_valid = UserUtil.validate_email(email)
    status = "valid" if is_valid else "invalid"
    icon = "✓" if is_valid == should_be_valid else "✗"
    print(f"{icon} '{email}' - {status}")


# ========== ПРИМЕР 5: Работа с UserService ==========
print("\n" + "=" * 60)
print("ПРИМЕР 5: Управление пользователями через UserService")
print("=" * 60)

# Очищаем сервис
UserService.clear_all()

# Создаем несколько пользователей
users_data = [
    (101, "Иван", "Петров", datetime.datetime(2000, 5, 15)),
    (102, "Мария", "Сидорова", datetime.datetime(1998, 3, 22)),
    (103, "Петр", "Иванов", datetime.datetime(2001, 12, 8)),
]

for user_id, name, surname, birthday in users_data:
    user = User(user_id, name, surname, birthday)
    user.email = UserUtil.generate_email(name, surname, "company.com")
    user.password = UserUtil.generate_password()
    UserService.add_user(user)
    print(f"✓ Добавлен пользователь: {name} {surname}")

print(f"\nВсего пользователей в системе: {UserService.get_number()}")

# Поиск пользователя
print("\n--- Поиск пользователя с ID 102 ---")
found_user = UserService.find_user(102)
if found_user:
    print(f"✓ Найден: {found_user.name} {found_user.surname}")
    print(f"  Email: {found_user.email}")
    print(f"  Возраст: {found_user.get_age()} лет")
else:
    print("✗ Пользователь не найден")

# Обновление пользователя
print("\n--- Обновление пользователя с ID 102 ---")
updated_user = User(102, "Мария", "Сидорова-Новая", datetime.datetime(1998, 3, 22))
updated_user.email = "maria.new@company.com"
if UserService.update_user(102, updated_user):
    updated = UserService.find_user(102)
    print(f"✓ Пользователь обновлен:")
    print(f"  Фамилия: {updated.surname}")
    print(f"  Email: {updated.email}")

# Удаление пользователя
print("\n--- Удаление пользователя с ID 101 ---")
if UserService.delete_user(101):
    print(f"✓ Пользователь удален")
    print(f"  Осталось пользователей: {UserService.get_number()}")


# ========== ПРИМЕР 6: Полная информация пользователя ==========
print("\n" + "=" * 60)
print("ПРИМЕР 6: Полная информация пользователя")
print("=" * 60)

user3 = UserService.find_user(102)
if user3:
    print("\n" + user3.get_details())


print("\n" + "=" * 60)
print("✓ Все примеры завершены!")
print("=" * 60)
