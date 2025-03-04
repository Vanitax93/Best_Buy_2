import pytest
from products import Product

def test_create_normal_product():
    """Test that creating a normal product works correctly."""
    product = Product("Test Product", price=100, quantity=50)
    assert product.name == "Test Product"
    assert product.price == 100
    assert product.quantity == 50
    assert product.is_active() == True

def test_create_product_with_invalid_name():
    """Test that creating a product with an empty name raises an exception."""
    with pytest.raises(ValueError, match="Name cannot be empty"):
        Product("", price=1450, quantity=100)

def test_create_product_with_negative_price():
    """Test that creating a product with a negative price raises an exception."""
    with pytest.raises(ValueError, match="Price cannot be negative"):
        Product("MacBook Air M2", price=-10, quantity=100)

def test_product_reaches_zero_quantity():
    """Test that a product becomes inactive when quantity reaches 0."""
    product = Product("Test Product", price=100, quantity=1)
    product.buy(1)
    assert product.get_quantity() == 0
    assert product.is_active() == False

def test_product_purchase():
    """Test that purchasing a product impacts quantity and returns the correct price."""
    product = Product("Test Product", price=200, quantity=10)
    total_price = product.buy(3)
    assert product.get_quantity() == 7
    assert total_price == 600

def test_buy_larger_quantity_than_available():
    """Test that buying more than available quantity raises an exception."""
    product = Product("Test Product", price=100, quantity=5)
    with pytest.raises(ValueError, match="Not enough quantity available"):
        product.buy(6)
