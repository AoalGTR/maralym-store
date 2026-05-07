"""
Electronic Device Shopping Cart System
Demonstrates OOP inheritance with a device store shopping cart application
"""

# ==================== Part 1: Base Device Class ====================
class Device:
    """
    Base class for all electronic devices.
    Defines common attributes and behaviors for all device types.
    """
    
    def __init__(self, name, price, stock, warranty_period):
        """
        Initialize a device with basic attributes.
        
        Args:
            name (str): The name of the device
            price (float): The price of the device
            stock (int): The number of units available
            warranty_period (int): Warranty period in months
        """
        self.name = name
        self.price = price
        self.stock = stock
        self.warranty_period = warranty_period
    
    def display_info(self):
        """Display the basic details of the device."""
        print(f"Device: {self.name}")
        print(f"Price: ${self.price:.2f}")
        print(f"Stock: {self.stock} units")
        print(f"Warranty: {self.warranty_period} months")
    
    def __str__(self):
        """String representation of the device."""
        return f"{self.name} - ${self.price:.2f} (Stock: {self.stock})"
    
    def apply_discount(self, discount_percentage):
        """
        Reduce the price by a specified discount percentage.
        
        Args:
            discount_percentage (float): The discount percentage (0-100)
        """
        discount_amount = (self.price * discount_percentage) / 100
        self.price -= discount_amount
        return self.price
    
    def is_available(self, amount):
        """
        Check if the device is available in the required quantity.
        
        Args:
            amount (int): The quantity to check
            
        Returns:
            bool: True if available, False otherwise
        """
        return self.stock >= amount
    
    def reduce_stock(self, amount):
        """
        Reduce the stock by the specified quantity.
        
        Args:
            amount (int): The quantity to reduce
        """
        if self.is_available(amount):
            self.stock -= amount
            return True
        return False


# ==================== Part 2: Derived Device Classes ====================
class Smartphone(Device):
    """Smartphone device with screen size and battery life."""
    
    def __init__(self, name, price, stock, warranty_period, screen_size, battery_life):
        """
        Initialize a smartphone.
        
        Args:
            screen_size (float): Screen size in inches
            battery_life (int): Battery life in hours
        """
        super().__init__(name, price, stock, warranty_period)
        self.screen_size = screen_size
        self.battery_life = battery_life
    
    def __str__(self):
        """String representation of smartphone."""
        return f"📱 {self.name} - ${self.price:.2f} (Screen: {self.screen_size}\" | Battery: {self.battery_life}h | Stock: {self.stock})"
    
    def display_info(self):
        """Display detailed smartphone information."""
        super().display_info()
        print(f"Screen Size: {self.screen_size} inches")
        print(f"Battery Life: {self.battery_life} hours")
        print()
    
    def make_call(self):
        """Simulate making a call."""
        return f"{self.name} is making a call..."
    
    def install_app(self):
        """Simulate installing an app."""
        return f"Installing an app on {self.name}..."


class Laptop(Device):
    """Laptop device with RAM size and processor speed."""
    
    def __init__(self, name, price, stock, warranty_period, ram_size, processor_speed):
        """
        Initialize a laptop.
        
        Args:
            ram_size (int): RAM size in GB
            processor_speed (float): Processor speed in GHz
        """
        super().__init__(name, price, stock, warranty_period)
        self.ram_size = ram_size
        self.processor_speed = processor_speed
    
    def __str__(self):
        """String representation of laptop."""
        return f"💻 {self.name} - ${self.price:.2f} (RAM: {self.ram_size}GB | Processor: {self.processor_speed}GHz | Stock: {self.stock})"
    
    def display_info(self):
        """Display detailed laptop information."""
        super().display_info()
        print(f"RAM Size: {self.ram_size} GB")
        print(f"Processor Speed: {self.processor_speed} GHz")
        print()
    
    def run_program(self):
        """Simulate running a program on the laptop."""
        return f"Running a program on {self.name}..."
    
    def use_keyboard(self):
        """Simulate typing on the keyboard."""
        return f"Typing on {self.name}'s keyboard..."


class Tablet(Device):
    """Tablet device with screen resolution and weight."""
    
    def __init__(self, name, price, stock, warranty_period, screen_resolution, weight):
        """
        Initialize a tablet.
        
        Args:
            screen_resolution (str): Screen resolution (e.g., "2048x1536")
            weight (float): Weight in grams
        """
        super().__init__(name, price, stock, warranty_period)
        self.screen_resolution = screen_resolution
        self.weight = weight
    
    def __str__(self):
        """String representation of tablet."""
        return f"📱 {self.name} - ${self.price:.2f} (Resolution: {self.screen_resolution} | Weight: {self.weight}g | Stock: {self.stock})"
    
    def display_info(self):
        """Display detailed tablet information."""
        super().display_info()
        print(f"Screen Resolution: {self.screen_resolution}")
        print(f"Weight: {self.weight} grams")
        print()
    
    def browse_internet(self):
        """Simulate browsing the internet."""
        return f"Browsing the internet on {self.name}..."
    
    def use_touchscreen(self):
        """Simulate using the touchscreen for navigation."""
        return f"Using touchscreen navigation on {self.name}..."


# ==================== Part 3: Shopping Cart System ====================
class Cart:
    """Shopping cart for managing device purchases."""
    
    def __init__(self):
        """Initialize an empty shopping cart."""
        self.items = []  # List of tuples: (device, amount)
        self.total_price = 0.0
    
    def add_device(self, device, amount):
        """
        Add a specified quantity of a device to the cart.
        
        Args:
            device (Device): The device to add
            amount (int): The quantity to add
            
        Returns:
            bool: True if added successfully, False otherwise
        """
        if not device.is_available(amount):
            print(f"❌ Insufficient stock for {device.name}. Available: {device.stock}, Requested: {amount}")
            return False
        
        # Check if device already in cart
        for i, (existing_device, existing_amount) in enumerate(self.items):
            if existing_device.name == device.name:
                self.items[i] = (existing_device, existing_amount + amount)
                self.total_price += device.price * amount
                print(f"✓ Updated {device.name} quantity to {existing_amount + amount}")
                return True
        
        # Add new device to cart
        self.items.append((device, amount))
        self.total_price += device.price * amount
        print(f"✓ Added {amount} x {device.name} to cart")
        return True
    
    def remove_device(self, device_name, amount):
        """
        Remove a specified quantity of a device from the cart.
        
        Args:
            device_name (str): The name of the device to remove
            amount (int): The quantity to remove
            
        Returns:
            bool: True if removed successfully, False otherwise
        """
        for i, (device, current_amount) in enumerate(self.items):
            if device.name == device_name:
                if current_amount > amount:
                    self.items[i] = (device, current_amount - amount)
                    self.total_price -= device.price * amount
                    print(f"✓ Removed {amount} x {device_name} from cart")
                else:
                    self.items.pop(i)
                    self.total_price -= device.price * current_amount
                    print(f"✓ Removed all {device_name} from cart")
                return True
        
        print(f"❌ {device_name} not found in cart")
        return False
    
    def get_total_price(self):
        """
        Retrieve the total price in the cart.
        
        Returns:
            float: The total price
        """
        return self.total_price
    
    def print_items(self):
        """Print all devices with their amounts in the cart."""
        if not self.items:
            print("\n📭 Your cart is empty!\n")
            return
        
        print("\n" + "="*70)
        print("🛒 SHOPPING CART CONTENTS")
        print("="*70)
        for device, amount in self.items:
            item_total = device.price * amount
            print(f"{device.name} × {amount} = ${item_total:.2f} (Unit: ${device.price:.2f})")
        print("-"*70)
        print(f"Total Price: ${self.total_price:.2f}")
        print("="*70 + "\n")
    
    def checkout(self):
        """
        Process checkout by reducing stock for all devices in cart.
        
        Returns:
            bool: True if checkout successful, False otherwise
        """
        if not self.items:
            print("❌ Cannot checkout - cart is empty!")
            return False
        
        # Check if all items are available
        for device, amount in self.items:
            if not device.is_available(amount):
                print(f"❌ Insufficient stock for {device.name}")
                return False
        
        # Reduce stock for all items
        print("\n" + "="*70)
        print("🧾 RECEIPT")
        print("="*70)
        for device, amount in self.items:
            device.reduce_stock(amount)
            item_total = device.price * amount
            print(f"{device.name} × {amount} = ${item_total:.2f}")
        
        print("-"*70)
        print(f"Total Amount: ${self.total_price:.2f}")
        print("="*70)
        print("✓ Thank you for your purchase!\n")
        
        # Clear cart after successful checkout
        self.items = []
        self.total_price = 0.0
        return True


# ==================== Part 4: Main Application ====================
def create_device_list():
    """
    Create a list of 20+ electronic devices.
    
    Returns:
        list: A list of Device objects (Smartphone, Laptop, Tablet)
    """
    devices = [
        # Smartphones
        Smartphone("iPhone 14", 999.99, 15, 12, 6.1, 20),
        Smartphone("iPhone 14 Pro", 1099.99, 10, 12, 6.1, 23),
        Smartphone("Samsung Galaxy S23", 899.99, 20, 12, 6.1, 22),
        Smartphone("Google Pixel 7", 599.99, 25, 12, 6.3, 24),
        Smartphone("OnePlus 11", 699.99, 18, 12, 6.7, 25),
        
        # Laptops
        Laptop("MacBook Pro 14", 1999.99, 8, 24, 16, 3.5),
        Laptop("MacBook Air M2", 1199.99, 12, 24, 8, 3.5),
        Laptop("Dell XPS 15", 1499.99, 14, 12, 16, 2.8),
        Laptop("HP Pavilion 15", 799.99, 20, 12, 8, 2.4),
        Laptop("Lenovo ThinkPad X1", 1299.99, 10, 12, 16, 3.2),
        
        # Tablets
        Tablet("iPad Pro 12.9", 1099.99, 10, 12, "2732x2048", 682),
        Tablet("iPad Air", 599.99, 15, 12, "2360x1640", 461),
        Tablet("iPad Mini", 499.99, 18, 12, "2266x1488", 293),
        Tablet("Samsung Galaxy Tab S8", 699.99, 12, 12, "2560x1600", 503),
        Tablet("Microsoft Surface Go 3", 399.99, 20, 12, "1920x1280", 544),
        
        # More Smartphones
        Smartphone("iPhone 13", 799.99, 22, 12, 6.1, 19),
        Smartphone("Xiaomi 12", 749.99, 16, 12, 6.28, 23),
        Smartphone("Motorola Edge 30", 499.99, 30, 12, 6.5, 20),
        
        # More Laptops
        Laptop("ASUS VivoBook 15", 599.99, 25, 12, 8, 2.6),
        Laptop("Acer Aspire 5", 749.99, 18, 12, 16, 2.9),
        
        # More Tablets
        Tablet("Amazon Fire HD 10", 149.99, 50, 6, "1920x1200", 465),
        Tablet("Lenovo Tab M10", 199.99, 30, 12, "1920x1200", 450),
    ]
    return devices


def display_devices(devices):
    """Display all available devices with options to add to cart."""
    print("\n" + "="*70)
    print("🏪 AVAILABLE DEVICES")
    print("="*70)
    for idx, device in enumerate(devices, 1):
        print(f"{idx:2d}. {device}")
    print("="*70 + "\n")


def show_menu():
    """Display the main menu and return user choice."""
    print("\n" + "="*70)
    print("📱 ELECTRONIC DEVICE SHOPPING CART SYSTEM 📱")
    print("="*70)
    print("1. Show Devices")
    print("2. Show Cart")
    print("3. Exit")
    print("="*70)
    choice = input("Select an option (1-3): ").strip()
    return choice


def main():
    """Main application loop."""
    devices = create_device_list()
    cart = Cart()
    
    while True:
        choice = show_menu()
        
        if choice == "1":
            # Show devices and allow adding to cart
            display_devices(devices)
            
            while True:
                user_input = input("Enter device number to add to cart (or 'back' to return to menu): ").strip().lower()
                
                if user_input == "back":
                    break
                
                try:
                    device_idx = int(user_input) - 1
                    if 0 <= device_idx < len(devices):
                        selected_device = devices[device_idx]
                        
                        # Ask for quantity
                        while True:
                            try:
                                quantity = int(input(f"Enter quantity for {selected_device.name}: ").strip())
                                if quantity > 0:
                                    cart.add_device(selected_device, quantity)
                                    break
                                else:
                                    print("❌ Please enter a positive number")
                            except ValueError:
                                print("❌ Invalid input. Please enter a valid number.")
                    else:
                        print("❌ Invalid device number. Please try again.")
                except ValueError:
                    print("❌ Invalid input. Please enter a valid number or 'back'.")
        
        elif choice == "2":
            # Show cart
            cart.print_items()
            
            if cart.items:
                checkout_choice = input("Would you like to proceed to checkout? (yes/no): ").strip().lower()
                if checkout_choice == "yes":
                    cart.checkout()
        
        elif choice == "3":
            print("\n✓ Thank you for shopping! Goodbye!\n")
            break
        
        else:
            print("❌ Invalid choice. Please select 1, 2, or 3.")


if __name__ == "__main__":
    main()
