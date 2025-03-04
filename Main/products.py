class Promotion:
    def __init__(self, name):
        """Initialize a promotion with a name."""
        self.name = name

    def apply_promotion(self, product, quantity) -> float:
        """Apply the promotion to a product and quantity (must be overridden by subclasses)."""
        raise NotImplementedError("Subclasses must implement apply_promotion")


class PercentDiscount(Promotion):
    def __init__(self, name, percent):
        """Initialize a percentage discount promotion."""
        super().__init__(name)
        self.percent = percent

    def apply_promotion(self, product, quantity) -> float:
        """Calculate total price with a percentage discount."""
        discount_factor = 1 - (self.percent / 100)
        return product.price * quantity * discount_factor


class SecondHalfPrice(Promotion):
    def __init__(self, name):
        """Initialize a second-item-at-half-price promotion."""
        super().__init__(name)

    def apply_promotion(self, product, quantity) -> float:
        """Calculate total price where every second item is half price."""
        full_price_pairs = quantity // 2
        single_items = quantity % 2
        pair_price = product.price + (product.price * 0.5)
        total = (full_price_pairs * pair_price) + (single_items * product.price)
        return total


class ThirdOneFree(Promotion):
    def __init__(self, name):
        """Initialize a buy-two-get-one-free promotion."""
        super().__init__(name)

    def apply_promotion(self, product, quantity) -> float:
        """Calculate total price where every third item is free."""
        sets_of_three = quantity // 3
        remaining_items = quantity % 3
        price_per_set = product.price * 2
        total = (sets_of_three * price_per_set) + (remaining_items * product.price)
        return total


class Product:
    def __init__(self, name, price, quantity):
        """Initialize a product with name, price, and quantity."""
        if not name:
            raise ValueError("Name cannot be empty")
        if price < 0:
            raise ValueError("Price cannot be negative")
        self.name = name
        self.price = price
        self.quantity = quantity
        self.active = True
        self.promotions = []

    def get_quantity(self):
        """Return the current quantity of the product."""
        return self.quantity

    def set_quantity(self, quantity):
        """Set the product quantity and update active status."""
        if quantity < 0:
            raise ValueError("Quantity below 0")
        self.quantity = quantity
        if self.quantity == 0:
            self.active = False

    def is_active(self):
        """Check if the product is active (quantity > 0)."""
        return self.active

    def activate(self):
        """Set the product as active."""
        self.active = True

    def deactivate(self):
        """Set the product as inactive."""
        self.active = False

    def get_promotions(self):
        """Return the list of promotions applied to the product."""
        return self.promotions

    def set_promotion(self, promotion):
        """Add a promotion to the product’s promotion list."""
        self.promotions.append(promotion)

    def clear_promotions(self):
        """Remove all promotions from the product."""
        self.promotions = []

    def show(self):
        """Return a string representation of the product."""
        base_info = f"{self.name}, Price: {self.price}, Quantity: {self.quantity}"
        if self.promotions:
            promo_names = ", ".join(promo.name for promo in self.promotions)
            return f"{base_info}, Promotions: {promo_names}"
        return base_info

    def buy(self, quantity):
        """Purchase a quantity of the product and return the total cost."""
        if quantity <= 0:
            raise ValueError("Purchase quantity must be positive")
        if not self.active:
            raise ValueError("Cannot buy inactive product")
        if quantity > self.quantity:
            raise ValueError("Not enough quantity available")

        if self.promotions:
            total_prices = [promo.apply_promotion(self, quantity) for promo in self.promotions]
            total_price = min(total_prices)
        else:
            total_price = self.price * quantity

        self.quantity -= quantity
        if self.quantity == 0:
            self.active = False

        return total_price


class NonStockedProduct(Product):
    def __init__(self, name, price):
        """Initialize a non-stocked product with unlimited quantity."""
        super().__init__(name, price, quantity=0)

    def set_quantity(self, quantity):
        """Prevent changing the quantity (always 0 for non-stocked)."""
        pass

    def buy(self, quantity):
        """Purchase a quantity of the non-stocked product and return the cost."""
        if quantity <= 0:
            raise ValueError("Purchase quantity must be positive")
        if not self.active:
            raise ValueError("Cannot buy inactive product")
        if self.promotions:
            total_prices = [promo.apply_promotion(self, quantity) for promo in self.promotions]
            return min(total_prices)
        return self.price * quantity

    def show(self):
        """Return a string representation of the non-stocked product."""
        base_info = f"{self.name}, Price: {self.price}, Non-Stocked (Unlimited)"
        if self.promotions:
            promo_names = ", ".join(promo.name for promo in self.promotions)
            return f"{base_info}, Promotions: {promo_names}"
        return base_info


class LimitedProduct(Product):
    def __init__(self, name, price, quantity, maximum):
        """Initialize a limited product with a maximum purchase limit per order."""
        super().__init__(name, price, quantity)
        self.maximum = maximum

    def buy(self, quantity):
        """Purchase a quantity of the limited product, enforcing the maximum limit."""
        if quantity <= 0:
            raise ValueError("Purchase quantity must be positive")
        if not self.active:
            raise ValueError("Cannot buy inactive product")
        if quantity > self.quantity:
            raise ValueError("Not enough quantity available")
        if quantity > self.maximum:
            raise ValueError(f"Cannot purchase more than {self.maximum} of {self.name} per order")

        if self.promotions:
            total_prices = [promo.apply_promotion(self, quantity) for promo in self.promotions]
            total_price = min(total_prices)
        else:
            total_price = self.price * quantity

        self.quantity -= quantity
        if self.quantity == 0:
            self.active = False

        return total_price

    def show(self):
        """Return a string representation of the limited product."""
        base_info = f"{self.name}, Price: {self.price}, Quantity: {self.quantity}, Max per order: {self.maximum}"
        if self.promotions:
            promo_names = ", ".join(promo.name for promo in self.promotions)
            return f"{base_info}, Promotions: {promo_names}"
        return base_info