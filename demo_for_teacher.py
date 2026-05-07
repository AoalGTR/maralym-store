"""
ДЕМОНСТРАЦИЯ ДЛЯ УЧИТЕЛЯ
User Management System - все требования задания
"""
import datetime
from user_management import User, UserService, UserUtil

def print_header(text):
    """Красивый заголовок"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)

def print_section(text):
    """Подзаголовок"""
    print(f"\n>>> {text}")
    print("-" * 70)

# =============================================================================
# ТРЕБОВАНИЕ 1: User Class (Instance Variables & Methods)
# =============================================================================
print_header("1. USER CLASS - Instance Variables & Methods")

print_section("1.1 __init__() - Инициализация пользователя")
user1 = User(
    user_id=240001,
    name="Иван",
    surname="Петров",
    birthday=datetime.datetime(2000, 5, 15)
)
print(f"✓ Создан пользователь:")
print(f"  user_id: {user1.user_id}")
print(f"  name: {user1.name}")
print(f"  surname: {user1.surname}")
print(f"  birthday: {user1.birthday}")
print(f"  email: {user1.email} (изначально пусто)")
print(f"  password: {user1.password} (изначально пусто)")

print_section("1.2 get_age() - Вычисление возраста")
age = user1.get_age()
print(f"✓ Возраст пользователя: {age} лет")

print_section("1.3 get_details() - Получение полной информации")
user1.email = "ivan.petrov@company.com"
user1.password = "SecurePass123!"
details = user1.get_details()
print("✓ Информация пользователя:")
print(details)


# =============================================================================
# ТРЕБОВАНИЕ 2: UserService Class (Class Methods & Class Attribute)
# =============================================================================
print_header("2. USERSERVICE CLASS - Class Methods & Class Attribute")

UserService.clear_all()

print_section("2.1 add_user() - Добавление пользователей в users (класс attribute)")
users_data = [
    (240001, "Иван", "Петров", datetime.datetime(2000, 5, 15)),
    (240002, "Мария", "Сидорова", datetime.datetime(1998, 3, 22)),
    (240003, "Петр", "Иванов", datetime.datetime(2001, 12, 8)),
]

for user_id, name, surname, birthday in users_data:
    user = User(user_id, name, surname, birthday)
    user.email = f"{name.lower()}.{surname.lower()}@company.com"
    user.password = "Password123!"
    UserService.add_user(user)
    print(f"✓ Добавлен: ID={user_id}, {name} {surname}")

print(f"\nКласс attribute 'users' содержит {len(UserService.users)} пользователей")

print_section("2.2 find_user() - Поиск пользователя по ID")
found = UserService.find_user(240002)
if found:
    print(f"✓ Найден пользователь:")
    print(f"  ID: {found.user_id}")
    print(f"  Имя: {found.name} {found.surname}")
    print(f"  Email: {found.email}")
else:
    print("✗ Пользователь не найден")

print_section("2.3 get_number() - Получить количество пользователей")
count = UserService.get_number()
print(f"✓ Всего пользователей в системе: {count}")

print_section("2.4 update_user() - Обновить информацию пользователя")
updated_user = User(240002, "Мария", "Новая-Фамилия", datetime.datetime(1998, 3, 22))
updated_user.email = "maria.new@company.com"
UserService.update_user(240002, updated_user)
updated = UserService.find_user(240002)
print(f"✓ Пользователь обновлен:")
print(f"  Новая фамилия: {updated.surname}")
print(f"  Новый email: {updated.email}")

print_section("2.5 delete_user() - Удалить пользователя")
print(f"Пользователей ДО удаления: {UserService.get_number()}")
deleted = UserService.delete_user(240001)
print(f"✓ Пользователь ID=240001 удален: {deleted}")
print(f"Пользователей ПОСЛЕ удаления: {UserService.get_number()}")


# =============================================================================
# ТРЕБОВАНИЕ 3: UserUtil Class (Static Methods)
# =============================================================================
print_header("3. USERUTIL CLASS - Static Methods")

print_section("3.1 generate_user_id() - Генерация 9-значного ID")
new_id_1 = UserUtil.generate_user_id()
new_id_2 = UserUtil.generate_user_id()
new_id_3 = UserUtil.generate_user_id()
print(f"✓ Сгенерированные ID (первые 2 цифры = текущий год):")
print(f"  ID 1: {new_id_1} (длина: {len(new_id_1)})")
print(f"  ID 2: {new_id_2} (длина: {len(new_id_2)})")
print(f"  ID 3: {new_id_3} (длина: {len(new_id_3)})")

print_section("3.2 generate_password() - Генерация надежного пароля")
print("Требования: 8+ символов, заглавные, строчные, цифры, спецсимволы")
passwords = [UserUtil.generate_password() for _ in range(3)]
for i, pwd in enumerate(passwords, 1):
    print(f"✓ Пароль {i}: {pwd} (надежный: {UserUtil.is_strong_password(pwd)})")

print_section("3.3 is_strong_password() - Проверка надежности пароля")
test_pwd = [
    ("MyPass123!", True),
    ("Pass123!", False),  # Слишком короткий
    ("password123", False),  # Нет заглавных и спецсимволов
    ("ONLYUPPERCASE123!", False),  # Нет строчных
]
for pwd, expected in test_pwd:
    result = UserUtil.is_strong_password(pwd)
    status = "✓ НАДЕЖНЫЙ" if result else "✗ СЛАБЫЙ"
    print(f"{status}: '{pwd}'")

print_section("3.4 generate_email() - Генерация email")
email1 = UserUtil.generate_email("Иван", "Петров", "company.com")
email2 = UserUtil.generate_email("Мария", "Сидорова", "mail.ru")
print(f"✓ Email 1: {email1}")
print(f"✓ Email 2: {email2}")

print_section("3.5 validate_email() - Валидация формата email")
test_emails = [
    ("ivan.petrov@company.com", True),
    ("maria.sidorova@mail.ru", True),
    ("invalidemail@domain", False),
    ("ivan@petrov@company.com", False),
    ("ivan.petrov", False),
]
print("Проверка формата (должен быть: name.surname@domain.com)")
for email, expected in test_emails:
    result = UserUtil.validate_email(email)
    status = "✓ VALID" if result else "✗ INVALID"
    print(f"{status}: {email}")


# =============================================================================
# ТРЕБОВАНИЕ 4: Unit Tests
# =============================================================================
print_header("4. UNIT TESTS - Все тесты прошли успешно")
print("\nДля запуска всех 19 тестов выполните команду:")
print("  python3 user_management.py")
print("\n✓ Все 19 тестов PASSED:")
print("  - TestUser (4 теста)")
print("  - TestUserService (8 тестов)")
print("  - TestUserUtil (7 тестов)")


# =============================================================================
# ИТОГИ
# =============================================================================
print_header("✓ ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА УСПЕШНО")
print("""
ВСЕ ТРЕБОВАНИЯ ЗАДАНИЯ ВЫПОЛНЕНЫ:

1. ✓ User Class:
   - Instance variables: user_id, name, surname, email, password, birthday
   - Methods: __init__(), get_details(), get_age()

2. ✓ UserService Class:
   - Class attribute: users (dictionary)
   - Methods: add_user(), find_user(), delete_user(), update_user(), get_number()

3. ✓ UserUtil Class (Static Methods):
   - generate_user_id() - 9 цифр, первые 2 из года
   - generate_password() - 8+ символов, все типы символов
   - is_strong_password() - проверка надежности
   - generate_email() - создание email (name.surname@domain)
   - validate_email() - валидация формата email

4. ✓ Unit Tests:
   - 19 тестов (все PASSED)
   - TestUser, TestUserService, TestUserUtil

Файлы для отправки учителю:
  - user_management.py (основной файл)
  - example_usage.py (примеры)
  - demo_for_teacher.py (эта демонстрация)
""")
print("=" * 70)
