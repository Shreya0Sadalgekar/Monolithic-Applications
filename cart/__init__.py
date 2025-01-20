import json
from cart import dao
from products import Product, get_product  # Ensure get_product is imported

class Cart:
    def __init__(self, id: int, username: str, contents: list[Product], cost: float):
        self.id = id
        self.username = username
        self.contents = contents
        self.cost = cost

    @staticmethod
    def load(data):
        # Convert dictionaries in contents to Product instances
        contents = [Product(**item) for item in data['contents']]
        return Cart(data['id'], data['username'], contents, data['cost'])

def get_cart(username: str) -> list[Product]:
    """Fetches the cart contents for a user."""
    cart_details = dao.get_cart(username)
    if cart_details is None:
        return []

    items = []
    for cart_detail in cart_details:
        contents = json.loads(cart_detail['contents'])
        items.extend(contents)

    # Fetch product details for all items
    products_list = [get_product(item['id']) for item in items]
    return products_list

def add_to_cart(username: str, product_id: int):
    """Adds a product to the user's cart."""
    dao.add_to_cart(username, product_id)

def remove_from_cart(username: str, product_id: int):
    """Removes a product from the user's cart."""
    dao.remove_from_cart(username, product_id)

def delete_cart(username: str):
    """Deletes the entire cart for the user."""
    dao.delete_cart(username)

