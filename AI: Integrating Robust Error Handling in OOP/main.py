class InvalidProductDataError(Exception):
    """Custom exception raised when a Product is assigned invalid data
    (e.g. a negative price or a negative/non-numeric quantity)."""
    pass


class Product:
    """Represents a product with a name, price, and quantity.

    price and quantity are exposed as properties so that every
    assignment - whether it happens in __init__ or later in the
    program - is routed through validation logic. This guarantees
    the object can never exist in an invalid state.
    """

    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price          # goes through the price setter
        self.quantity = quantity    # goes through the quantity setter

    # ---------- price ----------
    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise InvalidProductDataError(
                f"Price must be a number, got {type(value).__name__!r}."
            )
        if value < 0:
            raise InvalidProductDataError(
                f"Price cannot be negative (received {value})."
            )
        self._price = float(value)

    # ---------- quantity ----------
    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        if not isinstance(value, int) or isinstance(value, bool):
            raise InvalidProductDataError(
                f"Quantity must be an integer, got {type(value).__name__!r}."
            )
        if value < 0:
            raise InvalidProductDataError(
                f"Quantity cannot be negative (received {value})."
            )
        self._quantity = value


class InventoryManager:
    """Manages the collection of products and provides inventory operations."""

    def __init__(self, inventory=None):
        self.inventory = inventory if inventory is not None else []

    def add_product(self, product):
        """Adds a product object to the inventory list."""
        self.inventory.append(product)

    def update_quantity(self, name, new_quantity):
        """Updates the quantity of a product by name.

        Because Product.quantity is a validated property, an invalid
        new_quantity raises InvalidProductDataError here instead of
        silently corrupting the inventory.
        """
        for product in self.inventory:
            if product.name == name:
                product.quantity = new_quantity
                break

    def calculate_total_value(self):
        """Calculates the total monetary value of all inventory."""
        total = 0
        for product in self.inventory:
            total += product.price * product.quantity
        return total

    def display_inventory(self):
        """Prints the current inventory list."""
        for product in self.inventory:
            print(f"{product.name} - ${product.price:.2f} x {product.quantity}")


# Demo Usage
manager = InventoryManager()
manager.add_product(Product("Laptop", 1200.00, 5))
manager.add_product(Product("Mouse", 25.00, 20))
manager.update_quantity("Mouse", 18)

print("Current Inventory:")
manager.display_inventory()
print(f"\nTotal Inventory Value: ${manager.calculate_total_value():.2f}")

# --- Testing Invalid Input ---
print("\n--- Testing Invalid Input ---")
try:
    manager.inventory[0].quantity = -5
except Exception as e:
    print(f"Test result: {e}")
