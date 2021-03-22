from typing import Any


def validate_type(obj: Any, validating_type):
    if not isinstance(obj, validating_type) and obj is not None:
        try:
            validating_type(obj)
        except ValueError:
            return False
    return True
