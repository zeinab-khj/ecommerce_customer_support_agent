from .data import PRODUCTS


def search_products(
    query: str,
) -> dict:

    query = query.lower()

    matches = [
        product
        for product in PRODUCTS
        if query in product["name"].lower()
        or query in product["category"].lower()
    ]

    return {
        "success": True,
        "products": matches,
    }


def get_recommendations(
    user_id: str,
    category: str | None = None,
) -> dict:

    products = PRODUCTS

    if category:
        products = [
            product
            for product in products
            if product["category"] == category
        ]

    return {
        "success": True,
        "user_id": user_id,
        "recommendations": products[:3],
    }
