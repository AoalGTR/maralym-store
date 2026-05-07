import datetime
import random
import string
import re
import unittest
from typing import Optional, Dict


# ==================== User Class ====================
class User:
    """Represents a user with personal details."""
    
    def __init__(self, user_id: int, name: str, surname: str, birthday: datetime.datetime):
        """
        Initialize a User object.
        
        Args:
            user_id: Unique identifier for the user
            name: First name of the user
            surname: Last name of the user
            birthday: Birthday of the user (datetime object)
        """
        self.user_id = user_id
        self.name = name
        self.surname = surname
        self.birthday = birthday
        self.email = ""
        self.password = ""
    
    def get_details(self) -> str:
        """
        Returns a formatted string containing user details.
        
        Returns:
            Formatted string with user information
        """
        return (f"User ID: {self.user_id}\n"
                f"Name: {self.name} {self.surname}\n"
                f"Email: {self.email}\n"
                f"Birthday: {self.birthday.strftime('%Y-%m-%d')}\n"
                f"Age: {self.get_age()}")
    
    def get_age(self) -> int:
        """
        Computes and returns the user's age in years.
        
        Returns:
            Age of the user in years
        """
        today = datetime.datetime.now()
        age = today.year - self.birthday.year
        # Adjust if birthday hasn't occurred this year
        if (today.month, today.day) < (self.birthday.month, self.birthday.day):
            age -= 1
        return age


# ==================== UserService Class ====================
class UserService:
    """Service class to manage User objects."""
    
    users: Dict[int, User] = {}
    
    @classmethod
    def add_user(cls, user: User) -> None:
        """
        Adds a User object to the users dictionary.
        
        Args:
            user: User object to add
        """
        cls.users[user.user_id] = user
    
    @classmethod
    def find_user(cls, user_id: int) -> Optional[User]:
        """
        Searches for a user by user_id.
        
        Args:
            user_id: ID of the user to find
            
        Returns:
            User object if found, None otherwise
        """
        return cls.users.get(user_id)
    
    @classmethod
    def delete_user(cls, user_id: int) -> bool:
        """
        Removes a user from users by user_id.
        
        Args:
            user_id: ID of the user to delete
            
        Returns:
            True if deletion was successful, False if user not found
        """
        if user_id in cls.users:
            del cls.users[user_id]
            return True
        return False
    
    @classmethod
    def update_user(cls, user_id: int, user_update: User) -> bool:
        """
        Updates user attributes using user_update object.
        
        Args:
            user_id: ID of the user to update
            user_update: User object with updated information
            
        Returns:
            True if update was successful, False if user not found
        """
        if user_id in cls.users:
            user = cls.users[user_id]
            user.name = user_update.name
            user.surname = user_update.surname
            user.birthday = user_update.birthday
            if user_update.email:
                user.email = user_update.email
            if user_update.password:
                user.password = user_update.password
            return True
        return False
    
    @classmethod
    def get_number(cls) -> int:
        """
        Returns the number of users in the service.
        
        Returns:
            Number of users
        """
        return len(cls.users)
    
    @classmethod
    def clear_all(cls) -> None:
        """Clears all users (useful for testing)."""
        cls.users.clear()


# ==================== UserUtil Class ====================
class UserUtil:
    """Utility class providing static methods for user operations."""
    
    @staticmethod
    def generate_user_id() -> str:
        """
        Generates a unique 9-digit user_id.
        First two digits are from the current year (e.g., "24" for 2024).
        Remaining 7 digits are randomly generated.
        
        Returns:
            9-digit user ID as string
        """
        current_year = datetime.datetime.now().year
        year_digits = str(current_year)[-2:]  # Last 2 digits of year
        random_digits = ''.join(random.choices(string.digits, k=7))
        return year_digits + random_digits
    
    @staticmethod
    def generate_password() -> str:
        """
        Generates a strong password with minimum 8 characters.
        Includes at least 1 uppercase, 1 lowercase, 1 digit, and 1 special character.
        
        Returns:
            Generated password string
        """
        uppercase = random.choice(string.ascii_uppercase)
        lowercase = random.choice(string.ascii_lowercase)
        digit = random.choice(string.digits)
        special = random.choice(string.punctuation)
        
        # Generate remaining 4 characters randomly from all categories
        all_chars = string.ascii_letters + string.digits + string.punctuation
        remaining = ''.join(random.choices(all_chars, k=4))
        
        # Combine and shuffle
        password = list(uppercase + lowercase + digit + special + remaining)
        random.shuffle(password)
        return ''.join(password)
    
    @staticmethod
    def is_strong_password(password: str) -> bool:
        """
        Checks if a password is strong.
        Must be at least 8 characters long and include uppercase, lowercase, digit, and special character.
        
        Args:
            password: Password string to validate
            
        Returns:
            True if password is strong, False otherwise
        """
        if len(password) < 8:
            return False
        
        has_uppercase = any(c.isupper() for c in password)
        has_lowercase = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in string.punctuation for c in password)
        
        return has_uppercase and has_lowercase and has_digit and has_special
    
    @staticmethod
    def generate_email(name: str, surname: str, domain: str = "example.com") -> str:
        """
        Generates an email address using name and surname in lowercase.
        
        Args:
            name: First name of user
            surname: Last name of user
            domain: Email domain (default: "example.com")
            
        Returns:
            Generated email address (e.g., "john.doe@example.com")
        """
        return f"{name.lower()}.{surname.lower()}@{domain}"
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Validates if email follows the pattern name.surname@domain.com format.
        
        Args:
            email: Email address to validate
            
        Returns:
            True if email is valid, False otherwise
        """
        # Pattern: alphanumeric.alphanumeric@alphanumeric.alphanumeric
        pattern = r'^[a-zA-Z0-9]+\.[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z0-9]+$'
        return re.match(pattern, email) is not None


# ==================== Unit Tests ====================
class TestUser(unittest.TestCase):
    """Test cases for the User class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.birthday = datetime.datetime(2000, 5, 15)
        self.user = User(1, "John", "Doe", self.birthday)
    
    def test_user_initialization(self):
        """Test User initialization."""
        self.assertEqual(self.user.user_id, 1)
        self.assertEqual(self.user.name, "John")
        self.assertEqual(self.user.surname, "Doe")
        self.assertEqual(self.user.birthday, self.birthday)
        self.assertEqual(self.user.email, "")
        self.assertEqual(self.user.password, "")
    
    def test_get_details(self):
        """Test get_details method."""
        self.user.email = "john.doe@example.com"
        details = self.user.get_details()
        self.assertIn("John", details)
        self.assertIn("Doe", details)
        self.assertIn("john.doe@example.com", details)
        self.assertIn("2000-05-15", details)
    
    def test_get_age(self):
        """Test get_age method."""
        age = self.user.get_age()
        current_year = datetime.datetime.now().year
        expected_age = current_year - 2000
        # Adjust for birthday not yet occurred this year
        if (datetime.datetime.now().month, datetime.datetime.now().day) < (5, 15):
            expected_age -= 1
        self.assertEqual(age, expected_age)
    
    def test_get_age_birthday_today(self):
        """Test get_age when birthday is today."""
        today = datetime.datetime.now()
        user = User(2, "Jane", "Smith", 
                   datetime.datetime(today.year - 25, today.month, today.day))
        self.assertEqual(user.get_age(), 25)


class TestUserService(unittest.TestCase):
    """Test cases for the UserService class."""
    
    def setUp(self):
        """Set up test fixtures."""
        UserService.clear_all()
        self.user1 = User(1, "John", "Doe", datetime.datetime(2000, 5, 15))
        self.user2 = User(2, "Jane", "Smith", datetime.datetime(1998, 3, 22))
    
    def tearDown(self):
        """Clean up after tests."""
        UserService.clear_all()
    
    def test_add_user(self):
        """Test adding a user."""
        UserService.add_user(self.user1)
        self.assertEqual(UserService.get_number(), 1)
        self.assertIn(1, UserService.users)
    
    def test_find_user(self):
        """Test finding a user."""
        UserService.add_user(self.user1)
        found_user = UserService.find_user(1)
        self.assertIsNotNone(found_user)
        self.assertEqual(found_user.name, "John")
    
    def test_find_user_not_found(self):
        """Test finding a user that doesn't exist."""
        found_user = UserService.find_user(999)
        self.assertIsNone(found_user)
    
    def test_delete_user(self):
        """Test deleting a user."""
        UserService.add_user(self.user1)
        self.assertEqual(UserService.get_number(), 1)
        deleted = UserService.delete_user(1)
        self.assertTrue(deleted)
        self.assertEqual(UserService.get_number(), 0)
    
    def test_delete_user_not_found(self):
        """Test deleting a user that doesn't exist."""
        deleted = UserService.delete_user(999)
        self.assertFalse(deleted)
    
    def test_update_user(self):
        """Test updating a user."""
        UserService.add_user(self.user1)
        updated_user = User(1, "Johnny", "Doe", datetime.datetime(2000, 5, 15))
        updated_user.email = "johnny.doe@example.com"
        result = UserService.update_user(1, updated_user)
        self.assertTrue(result)
        found_user = UserService.find_user(1)
        self.assertEqual(found_user.name, "Johnny")
        self.assertEqual(found_user.email, "johnny.doe@example.com")
    
    def test_update_user_not_found(self):
        """Test updating a user that doesn't exist."""
        result = UserService.update_user(999, self.user1)
        self.assertFalse(result)
    
    def test_get_number(self):
        """Test getting number of users."""
        self.assertEqual(UserService.get_number(), 0)
        UserService.add_user(self.user1)
        self.assertEqual(UserService.get_number(), 1)
        UserService.add_user(self.user2)
        self.assertEqual(UserService.get_number(), 2)


class TestUserUtil(unittest.TestCase):
    """Test cases for the UserUtil class."""
    
    def test_generate_user_id(self):
        """Test generating user ID."""
        user_id = UserUtil.generate_user_id()
        self.assertEqual(len(user_id), 9)
        self.assertTrue(user_id.isdigit())
        # First two digits should be from current year
        current_year_digits = str(datetime.datetime.now().year)[-2:]
        self.assertTrue(user_id.startswith(current_year_digits))
    
    def test_generate_password(self):
        """Test generating password."""
        password = UserUtil.generate_password()
        self.assertGreaterEqual(len(password), 8)
        self.assertTrue(UserUtil.is_strong_password(password))
    
    def test_is_strong_password_valid(self):
        """Test is_strong_password with valid password."""
        strong_passwords = [
            "Pass123!word",
            "SecureP@ss1",
            "Qwerty1@zxc",
            "MyPass123#"
        ]
        for password in strong_passwords:
            self.assertTrue(UserUtil.is_strong_password(password), 
                          f"Password '{password}' should be strong")
    
    def test_is_strong_password_invalid(self):
        """Test is_strong_password with invalid passwords."""
        weak_passwords = [
            "pass123!",  # No uppercase
            "PASS123!",  # No lowercase
            "Password!",  # No digit
            "Pass1234",  # No special character
            "Pass1!",    # Too short
        ]
        for password in weak_passwords:
            self.assertFalse(UserUtil.is_strong_password(password),
                           f"Password '{password}' should not be strong")
    
    def test_generate_email(self):
        """Test email generation."""
        email = UserUtil.generate_email("John", "Doe")
        self.assertEqual(email, "john.doe@example.com")
        
        email_custom = UserUtil.generate_email("Jane", "Smith", "company.com")
        self.assertEqual(email_custom, "jane.smith@company.com")
    
    def test_validate_email_valid(self):
        """Test email validation with valid emails."""
        valid_emails = [
            "john.doe@example.com",
            "jane.smith@company.org",
            "user123.last456@domain.co",
            "a.b@test.net"
        ]
        for email in valid_emails:
            self.assertTrue(UserUtil.validate_email(email),
                          f"Email '{email}' should be valid")
    
    def test_validate_email_invalid(self):
        """Test email validation with invalid emails."""
        invalid_emails = [
            "john.doe@example",  # Missing domain extension
            "johndoe@example.com",  # Missing dot before @
            "john@doe@example.com",  # Multiple @
            "john.doe",  # Missing @
            "john.doe@.com",  # Missing domain name
            "john..doe@example.com",  # Double dots
        ]
        for email in invalid_emails:
            self.assertFalse(UserUtil.validate_email(email),
                           f"Email '{email}' should be invalid")


# ==================== Example Usage ====================
def main():
    """Demonstrates usage of User, UserService, and UserUtil classes."""
    print("=== User Management System Demo ===\n")
    
    # Generate user IDs and email
    print("1. Generating user ID:")
    user_id = UserUtil.generate_user_id()
    print(f"   Generated User ID: {user_id}")
    
    print("\n2. Generating password:")
    password = UserUtil.generate_password()
    print(f"   Generated Password: {password}")
    print(f"   Is Strong: {UserUtil.is_strong_password(password)}")
    
    print("\n3. Creating users:")
    user1 = User(int(user_id), "John", "Doe", datetime.datetime(2000, 5, 15))
    user1.email = UserUtil.generate_email("John", "Doe", "company.com")
    user1.password = password
    print(f"   User 1 created: {user1.name} {user1.surname}")
    
    user2 = User(240000002, "Jane", "Smith", datetime.datetime(1998, 3, 22))
    user2.email = UserUtil.generate_email("Jane", "Smith", "company.com")
    user2.password = UserUtil.generate_password()
    print(f"   User 2 created: {user2.name} {user2.surname}")
    
    print("\n4. Adding users to service:")
    UserService.add_user(user1)
    UserService.add_user(user2)
    print(f"   Total users: {UserService.get_number()}")
    
    print("\n5. Finding user:")
    found = UserService.find_user(int(user_id))
    if found:
        print(f"   Found user: {found.name} {found.surname}")
        print(f"   Age: {found.get_age()}")
    
    print("\n6. User details:")
    print(user1.get_details())
    
    print("\n7. Validating email:")
    test_email = "john.doe@company.com"
    print(f"   Email: {test_email}")
    print(f"   Valid: {UserUtil.validate_email(test_email)}")


if __name__ == "__main__":
    # Run unit tests
    unittest.main(argv=[''], exit=False, verbosity=2)
    
    # Run demo (commented to avoid clutter during tests)
    # main()
