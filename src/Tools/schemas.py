TOOL_SCHEMAS = [
    {
        "name": "cancel_order",
        "description": "Cancel an order when cancellation is allowed.",
        "parameters": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": "The order identifier.",
                },
                "reason": {
                    "type": "string",
                    "description": "Reason for cancellation.",
                },
            },
            "required": ["order_id"],
        },
    },
    {
        "name": "initiate_exchange",
        "description": "Initiate an exchange for an item in an order.",
        "parameters": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": "The order identifier.",
                },
                "item_sku": {
                    "type": "string",
                    "description": "SKU of the item to exchange.",
                },
                "new_variant": {
                    "type": "string",
                    "description": "The requested replacement variant.",
                },
            },
            "required": [
                "order_id",
                "item_sku",
                "new_variant",
            ],
        },
    },
    {
        "name": "get_order_status",
        "description": "Retrieve the current status of an order.",
        "parameters": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": "The order identifier.",
                },
                "user_id": {
                    "type": "string",
                    "description": "The customer identifier.",
                },
            },
            "required": [
                "order_id",
                "user_id",
            ],
        },
    },
    {
        "name": "initiate_return",
        "description": "Initiate a return for an order.",
        "parameters": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": "The order identifier.",
                },
                "reason": {
                    "type": "string",
                    "description": "Reason for the return.",
                },
                "item_sku": {
                    "type": "string",
                    "description": "Optional SKU of the returned item.",
                },
            },
            "required": [
                "order_id",
                "reason",
            ],
        },
    },
    {
        "name": "search_products",
        "description": "Search the product catalog.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Product search query.",
                },
            },
            "required": ["query"],
        },
    },
    {
        "name": "log_payment_dispute",
        "description": "Log a payment dispute for a customer.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "The customer identifier.",
                },
                "transaction_id": {
                    "type": "string",
                    "description": "The transaction identifier.",
                },
                "reason": {
                    "type": "string",
                    "description": "Reason for the payment dispute.",
                },
            },
            "required": [
                "user_id",
                "transaction_id",
                "reason",
            ],
        },
    },
    {
        "name": "update_account",
        "description": "Update an allowed customer account field.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "The customer identifier.",
                },
                "field": {
                    "type": "string",
                    "enum": [
                        "shipping_address",
                        "email",
                        "phone",
                        "password",
                    ],
                    "description": "Account field to update.",
                },
                "value": {
                    "type": "string",
                    "description": "New value for the account field.",
                },
            },
            "required": [
                "user_id",
                "field",
                "value",
            ],
        },
    },
    {
        "name": "log_complaint",
        "description": "Log a customer complaint.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "The customer identifier.",
                },
                "complaint": {
                    "type": "string",
                    "description": "The complaint text.",
                },
            },
            "required": [
                "user_id",
                "complaint",
            ],
        },
    },
    {
        "name": "add_to_cart",
        "description": "Add a product to the customer's cart.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "The customer identifier.",
                },
                "item_sku": {
                    "type": "string",
                    "description": "Product SKU.",
                },
                "quantity": {
                    "type": "integer",
                    "description": "Quantity to add.",
                },
            },
            "required": [
                "user_id",
                "item_sku",
                "quantity",
            ],
        },
    },
    {
        "name": "update_cart_qty",
        "description": "Update the quantity of an item in the cart.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "The customer identifier.",
                },
                "item_sku": {
                    "type": "string",
                    "description": "Product SKU.",
                },
                "quantity": {
                    "type": "integer",
                    "description": "New quantity.",
                },
            },
            "required": [
                "user_id",
                "item_sku",
                "quantity",
            ],
        },
    },
    {
        "name": "escalate_to_agent",
        "description": "Escalate a customer issue to a human support agent.",
        "parameters": {
            "type": "object",
            "properties": {
                "reason": {
                    "type": "string",
                    "description": "Reason for escalation.",
                },
                "priority": {
                    "type": "string",
                    "description": "Escalation priority.",
                },
                "context_summary": {
                    "type": "string",
                    "description": "Optional summary of the issue.",
                },
            },
            "required": [
                "reason",
                "priority",
            ],
        },
    },
    {
        "name": "get_recommendations",
        "description": "Get product recommendations for a customer.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "The customer identifier.",
                },
                "category": {
                    "type": "string",
                    "description": "Optional product category.",
                },
            },
            "required": ["user_id"],
        },
    },
]
