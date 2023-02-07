import re

from fastapi import HTTPException


def is_valid_phone_number(phone_number: str):

    validate_phone_number_pattern = "^\+?77([0124567][0-8]\d{7})$"
    result = re.match(validate_phone_number_pattern, phone_number)

    return result


def is_owner(user_role: str):
    if user_role != "OWNER":
        raise HTTPException(status_code=403, detail="You don't have permission!")
