from .data import ACCOUNTS


ALLOWED_ACCOUNT_FIELDS = {
    "shipping_address",
    "email",
    "phone",
    "password",
}


def update_account(
    user_id: str,
    field: str,
    value: str,
) -> dict:

    if field not in ALLOWED_ACCOUNT_FIELDS:
        return {
            "success": False,
            "error": "Unsupported account field.",
        }

    if user_id not in ACCOUNTS:
        return {
            "success": False,
            "error": "User not found.",
        }

    ACCOUNTS[user_id][field] = value

    return {
        "success": True,
        "user_id": user_id,
        "updated_field": field,
    }
