from typing import Callable, Any

from .account_tools import update_account
from .cart_tools import add_to_cart, update_cart_qty
from .order_tools import (
    cancel_order,
    get_order_status,
    initiate_exchange,
    initiate_return,
)
from .product_tools import (
    get_recommendations,
    search_products,
)
from .support_tools import (
    escalate_to_agent,
    log_complaint,
    log_payment_dispute,
)


ToolFunction = Callable[..., Any]


TOOL_REGISTRY: dict[str, ToolFunction] = {
    "cancel_order": cancel_order,
    "initiate_exchange": initiate_exchange,
    "get_order_status": get_order_status,
    "initiate_return": initiate_return,
    "search_products": search_products,
    "log_payment_dispute": log_payment_dispute,
    "update_account": update_account,
    "log_complaint": log_complaint,
    "add_to_cart": add_to_cart,
    "update_cart_qty": update_cart_qty,
    "escalate_to_agent": escalate_to_agent,
    "get_recommendations": get_recommendations,
}
