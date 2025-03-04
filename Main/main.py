from products import Product, NonStockedProduct, LimitedProduct, PercentDiscount, SecondHalfPrice, ThirdOneFree
from store import Store

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


def start(store):
    """Run the interactive Best Buy store interface."""
    while True:
        print("\n=== Welcome to Best Buy ===")
        print("1. List all products in store")
        print("2. Show total amount in store")
        print("3. Make an order")
        print("4. Quit")

        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            display_product_list(store)
        elif choice == "2":
            show_total_quantity(store)
        elif choice == "3":
            make_order(store)
        elif choice == "4":
            quit_store()
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")


def display_product_list(store):
    """Display all active products in the store."""
    print(f"\n{store.display_products()}")


def show_total_quantity(store):
    """Show the total quantity of items in the store."""
    total = store.get_total_quantity()
    print(f"Total quantity in store: {total}")


def make_order(store):
    """Process a customer order with automatic shipping fee."""
    active_products = store.get_all_products()
    if not active_products:
        print("No active products available to order.")
    else:
        print("\nActive Products:")
        for i, product in enumerate(active_products, 1):
            print(f"{i}. {product.show()} (Available: {product.get_quantity()})")

        shopping_list = build_shopping_list(active_products)
        if shopping_list:
            process_order(store, shopping_list)
        else:
            print("No items ordered.")


def build_shopping_list(active_products):
    """Build a shopping list from user input."""
    shopping_list = []
    while True:
        try:
            item_num = input("Enter product number to order (or 'done' to finish): ").strip()
            if item_num.lower() == "done":
                break
            index = int(item_num) - 1
            if 0 <= index < len(active_products):
                quantity = int(input(f"Enter quantity for {active_products[index].name}: "))
                shopping_list.append((active_products[index], quantity))
                print("Product added to list!")
            else:
                print("Invalid product number.")
        except ValueError:
            print("Please enter a valid number or 'done'.")
    return shopping_list


def process_order(store, shopping_list):
    """Process the order and display the total cost with shipping."""
    try:
        total_cost, order_details = store.order(shopping_list, include_shipping=True)
        print(f"Order completed! Total cost: ${total_cost:.2f} (includes ${store.shipping_fee:.2f} shipping fee)")
        print("\nShopping List:")
        for item, qty, cost in order_details:
            item_name = item if isinstance(item, str) else item.name
            unit_price = cost / qty if qty > 0 else cost
            print(f"- {item_name}: {qty} x ${unit_price:.2f} = ${cost:.2f}")
    except ValueError as e:
        print(f"Order failed: {e}")


def quit_store():
    """Exit the store interface."""
    print("Thank you, have a nice day!")

if __name__ == "__main__":
    start(best_buy)