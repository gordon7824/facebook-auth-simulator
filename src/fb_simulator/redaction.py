"""敏感字段脱敏。"""

import re
from typing import Any, Dict

SENSITIVE_FIELDS = {
    "password", "token", "nonce", "phone", "uid", "device_id",
    "oauth_token", "session_token", "push_token"
}


def redact_field(value: Any, field_name: str) -> Any:
    """脱敏单个字段。"""
    if not isinstance(value, str):
        return value
    if field_name.lower() in SENSITIVE_FIELDS:
        if "phone" in field_name.lower():
            return re.sub(r"(\+\d{2,3})(\d+)(\d{4})", r"\1***\3", value)
        return "<redacted>"
    return value


def redact_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    """递归脱敏字典。"""
    if not isinstance(data, dict):
        return data
    result = {}
    for key, value in data.items():
        if isinstance(value, dict):
            result[key] = redact_dict(value)
        elif isinstance(value, list):
            result[key] = [redact_dict(item) if isinstance(item, dict) else redact_field(item, key) for item in value]
        else:
            result[key] = redact_field(value, key)
    return result
