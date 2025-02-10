import json
import time

def serialize(value):
    """Serialize Python objects to JSON strings."""
    try:
        return json.dumps(value)
    except (TypeError, ValueError) as e:
        raise ValueError(f"Serialization Error: {e}")

def deserialize(value):
    """Deserialize JSON strings back to Python objects."""
    try:
        return json.loads(value) if value else None
    except json.JSONDecodeError as e:
        raise ValueError(f"Deserialization Error: {e}")

def current_timestamp():
    """Returns the current UNIX timestamp."""
    return int(time.time())

def is_active_ttl_enabled(env_value):
    """Convert environment variable string to boolean."""
    return str(env_value).lower() in ("true", "1", "yes")
