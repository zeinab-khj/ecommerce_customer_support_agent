from .data import ORDERS


def get_order_status(
    order_id: str,
    user_id: str,
) -> dict:

    order = ORDERS.get(order_id)

    if order is None:
        return {
            "success": False,
            "error": "Order not found.",
        }

    if order["user_id"] != user_id:
        return {
            "success": False,
            "error": "Order does not belong to this user.",
        }

    return {
        "success": True,
        "order_id": order_id,
        "status": order["status"],
    }


def cancel_order(
    order_id: str,
    reason: str | None = None,
) -> dict:

    order = ORDERS.get(order_id)

    if order is None:
        return {
            "success": False,
            "error": "Order not found.",
        }

    if order["status"] in {"shipped", "delivered"}:
        return {
            "success": False,
            "error": "Order cannot be cancelled at this stage.",
        }

    order["status"] = "cancelled"

    return {
        "success": True,
        "order_id": order_id,
        "status": "cancelled",
        "reason": reason,
    }


def initiate_return(
    order_id: str,
    reason: str,
    item_sku: str | None = None,
) -> dict:

    order = ORDERS.get(order_id)

    if order is None:
        return {
            "success": False,
            "error": "Order not found.",
        }

    return {
        "success": True,
        "order_id": order_id,
        "item_sku": item_sku,
        "reason": reason,
        "status": "return_requested",
    }


def initiate_exchange(
    order_id: str,
    item_sku: str,
    new_variant: str,
) -> dict:

    order = ORDERS.get(order_id)

    if order is None:
        return {
            "success": False,
            "error": "Order not found.",
        }

    return {
        "success": True,
        "order_id": order_id,
        "item_sku": item_sku,
        "new_variant": new_variant,
        "status": "exchange_requested",
    }
