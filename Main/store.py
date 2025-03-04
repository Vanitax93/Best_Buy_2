from products import Product, NonStockedProduct, LimitedProduct, PercentDiscount, SecondHalfPrice, ThirdOneFree


class Store:
    def __init__(self, products, shipping_fee=10.0):
        self.products = products
        self.shipping_fee = shipping_fee  # Default shipping fee

    def add_product(self, product):
        self.products.append(product)

    def remove_product(self, product):
        if product in self.products:
            self.products.remove(product)

    def get_total_quantity(self):
        return sum(product.get_quantity() for product in self.products)

    def get_all_products(self):
        return [product for product in self.products if product.is_active()]

    def order(self, shopping_list, include_shipping=True):
        total_price = 0.0
        order_details = []
        for product, quantity in shopping_list:
            if product in self.products and product.is_active():
                cost = product.buy(quantity)
                total_price += cost
                order_details.append((product, quantity, cost))
            else:
                raise ValueError(f"Product {product.name} not available or inactive")

        # Add shipping fee if applicable
        if include_shipping and shopping_list:  # Only add shipping if there’s an order
            total_price += self.shipping_fee
            order_details.append(("Shipping Fee", 1, self.shipping_fee))

        return total_price, order_details

    def display_products(self):
        active_products = self.get_all_products()
        if not active_products:
            return "No active products available."
        result = "Active Products:\n"
        for i, product in enumerate(active_products, 1):
            result += f"{i}. {product.show()} (Available: {product.get_quantity()})\n"
        return result.strip()


def main():
    # setup initial stock of inventory
    product_list = [
        Product("MacBook Air M2", price=1450, quantity=100),
        Product("Bose QuietComfort Earbuds", price=250, quantity=500),
        Product("Google Pixel 7", price=500, quantity=250),
        NonStockedProduct("Windows License", price=125),
        LimitedProduct("Special Edition Pokémon USB Drive", price=50, quantity=10, maximum=2)
    ]
    # Create promotion catalog
    second_half_price = SecondHalfPrice("Second item for half price!")
    third_one_free = ThirdOneFree("Third One Is Free!")
    thirty_percent = PercentDiscount("30% off!", percent=30)

    # Add promotions to products
    product_list[0].set_promotion(second_half_price)
    product_list[0].set_promotion(thirty_percent)
    product_list[1].set_promotion(third_one_free)
    product_list[3].set_promotion(thirty_percent)

    best_buy = Store(product_list)

    print(best_buy.display_products())
    print(f"\nTotal quantity: {best_buy.get_total_quantity()}")
    total, details = best_buy.order([(product_list[0], 2)], include_shipping=True)
    print(f"Order cost: ${total:.2f}")
    for item, qty, cost in details:
        print(f"- {item if isinstance(item, str) else item.name}: {qty} x ${cost / qty:.2f} = ${cost:.2f}")


if __name__ == "__main__":
    main()