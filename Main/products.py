class Product:
    def __init__(self, name, price, quantity):
        if not name:
            raise ValueError("Name cannot be empty")
        if price < 0:
            raise ValueError("Price cannot be negative")
        self.name = name
        self.price = price
        self.quantity = quantity
        self.active = True

    def get_quantity(self):
        return self.quantity

    def set_quantity(self, quantity):
        if quantity < 0:
            raise ValueError("Quantity below 0")
        self.quantity = quantity
        if self.quantity == 0:
            self.active = False

    def is_active(self):
        return self.active

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def show(self):
        return f"{self.name}, Price: {self.price}, Quantity: {self.quantity}"

    def buy(self, quantity):
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        if not self.active:
            raise ValueError("Cannot buy inactive product")
        if quantity > self.quantity:
            raise ValueError("Not enough quantity available")

        total_price = self.price * quantity
        self.quantity -= quantity

        if self.quantity == 0:
            self.active = False

        return total_price

class NonStockedProduct(Product):
    def __init__(self, name, price):
        super().__init__(name, price, quantity=0)  # Quantity is always 0

    def set_quantity(self, quantity):
        # Override to prevent quantity changes
        pass

    def buy(self, quantity):
        if quantity <= 0:
            raise ValueError("Purchase quantity must be positive")
        if not self.active:
            raise ValueError("Cannot buy inactive product")
        # No quantity check since it's non-stocked
        return self.price * quantity

    def show(self):
        return f"{self.name}, Price: {self.price}, Non-Stocked (Unlimited)"


class LimitedProduct(Product):
    def __init__(self, name, price, quantity, maximum):
        super().__init__(name, price, quantity)
        self.maximum = maximum

    def buy(self, quantity):
        if quantity <= 0:
            raise ValueError("Purchase quantity must be positive")
        if not self.active:
            raise ValueError("Cannot buy inactive product")
        if quantity > self.quantity:
            raise ValueError("Not enough quantity available")
        if quantity > self.maximum:
            raise ValueError(f"Cannot purchase more than {self.maximum} of {self.name} per order")

        total_price = self.price * quantity
        self.quantity -= quantity

        if self.quantity == 0:
            self.active = False

        return total_price

    def show(self):
        return f"{self.name}, Price: {self.price}, Quantity: {self.quantity}, Max per order: {self.maximum}"


if __name__ == "__main__":
    import store
    product_list = [
        Product("MacBook Air M2", price=1450, quantity=100),
        Product("Bose QuietComfort Earbuds", price=250, quantity=500),
        Product("Google Pixel 7", price=500, quantity=250),
        NonStockedProduct("Windows License", price=125),
        LimitedProduct("Shipping", price=9.99, quantity=250, maximum=1)
    ]
    best_buy = store.Store(product_list)