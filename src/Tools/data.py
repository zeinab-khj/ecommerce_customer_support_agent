ORDERS = {
    "ORD-1001": {
        "user_id": "USER-001",
        "status": "shipped",
        "items": [
            {
                "sku": "SKU-001",
                "name": "Wireless Headphones",
                "variant": "Black",
            }
        ],
    },
    "ORD-1002": {
        "user_id": "USER-002",
        "status": "processing",
        "items": [
            {
                "sku": "SKU-002",
                "name": "Running Shoes",
                "variant": "Size 42",
            }
        ],
    },
}


PRODUCTS = [
    {
        "sku": "SKU-001",
        "name": "Wireless Headphones",
        "category": "electronics",
        "price": 79.99,
        "variants": ["Black", "White"],
    },
    {
        "sku": "SKU-002",
        "name": "Running Shoes",
        "category": "sports",
        "price": 64.99,
        "variants": ["Size 41", "Size 42", "Size 43"],
    },
]


CARTS = {
    "USER-001": [],
    "USER-002": [],
}


ACCOUNTS = {
    "USER-001": {
        "email": "user001@example.com",
        "phone": "+10000000001",
        "shipping_address": "123 Main Street",
    },
    "USER-002": {
        "email": "user002@example.com",
        "phone": "+10000000002",
        "shipping_address": "456 Oak Street",
    },
}
