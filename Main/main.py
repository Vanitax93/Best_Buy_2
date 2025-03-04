from products import Product
from store import Store

product_list = [
    Product("MacBook Air M2", price=1450, quantity=100),
    Product("Bose QuietComfort Earbuds", price=250, quantity=500),
    Product("Google Pixel 7", price=500, quantity=250)
]
best_buy = Store(product_list)


def start(store):
    """Start the interface."""
    while True:
        print("\n=== Welcome to Best Buy ===")
        print("1. List all products in store")
        print("2. Show total amount in store")
        print("3. Make an order")
        print("4. Quit")

        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            # List all active products
            active_products = store.get_all_products()
            if not active_products:
                print("No active products available.")
            else:
                print("\nActive Products:")
                for i, product in enumerate(active_products, 1):
                    print(f"{i}. {product.show()}")

        elif choice == "2":
            # Show total quantity
            total = store.get_total_quantity()
            print(f"Total quantity in store: {total}")

        elif choice == "3":
            # Make an order
            active_products = store.get_all_products()
            if not active_products:
                print("No active products available to order.")
            else:
                print("\nActive Products:")
                for i, product in enumerate(active_products, 1):
                    print(f"{i}. {product.show()} (Available: {product.get_quantity()})")

# Not in assignment but i also added a shopping list at the end of the order to show the total price
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

                if shopping_list:
                    try:
                        total_cost = store.order(shopping_list)
                        print(f"Order completed! Total cost: ${total_cost: 3}")
                    except ValueError as e:
                        print(f"Order failed: {e}")

        elif choice == "4":
            # Quit
            print("Thank you, have a nice day!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 4.")


if __name__ == "__main__":
    start(best_buy)