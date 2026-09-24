from .data import CARTS


def add_to_cart(
    user_id: str,
    item_sku: str,
    quantity: int,
) -> dict:

    CARTS.setdefault(user_id, [])

    CARTS[user_id].append(
        {
            "item_sku": item_sku,
            "quantity": quantity,
        }
    )

    return {
        "success": True,
        "user_id": user_id,
        "cart": CARTS[user_id],
    }


def update_cart_qty(
    user_id: str,
    item_sku: str,
    quantity: int,
) -> dict:

    cart = CARTS.get(user_id, [])

    for item in cart:
        if item["item_sku"] == item_sku:
            item["quantity"] = quantity

            return {
                "success": True,
                "user_id": user_id,
                "cart": cart,
            }

    return {
        "success": False,
        "error": "Item not found in cart.",
    }
