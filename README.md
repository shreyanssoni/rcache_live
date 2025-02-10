# Redis Cache Library

[![PyPI version](https://badge.fury.io/py/rcache-live.svg)](https://pypi.org/project/rcache-live/)

## Overview
This is a simple and efficient Redis caching library for Python that supports **Active TTL**. It provides an easy-to-use interface for storing, retrieving, and managing cached data while automatically refreshing TTL for active records. The library is designed for caching any type of data, not just user sessions, making it a versatile solution for various use cases.

## Features
- **Dictionary-style access** (`cache[key] = value` and `cache[key]`)
- **Auto field updates** via `update()`
- **Bulk insert shortcut** via `add()`
- **Configurable Redis Credentials** via `config.py`
- **Custom TTL per Record** (default and per-key support)
- **Active TTL** (Resets TTL when a record is accessed or updated)
- **Efficient Background Cleanup** for stale records
- **Simple API for CRUD Operations**

## Installation
```sh
pip install rcache-live
```

## Usage

### Initialize the Cache
```python
from rcache_live.redis_cache import RedisCache

# Create a Redis cache instance
cache = RedisCache()
```

### Set and Get a Record (Dictionary-Style Access)
```python
cache["user:123"] = {"name": "John Doe", "age": 30}  # Set a record
print(cache["user:123"])  # Get a record
```

### Auto Field Updates
```python
cache["user:123"] = {"name": "John Doe", "age": 30}
cache.update("user:123", age=31)  # Update only the age field
print(cache["user:123"])  # Output: {'name': 'John Doe', 'age': 31}
```

### Bulk Insert Shortcut
```python
cache.add(user1={"name": "Alice"}, user2={"name": "Bob"})
print(cache["user1"])  # Output: {'name': 'Alice'}
print(cache["user2"])  # Output: {'name': 'Bob'}
```

### Delete a Record
```python
del cache["user:123"]
```

### Get All Records
```python
all_records = cache.get_all_records()
print(all_records)
```

### Cleanup Inactive Records
```python
cache.cleanup_inactive_records(past_minutes=60)
```

## Active TTL - Unique Feature
### What is Active TTL?
Active TTL is a feature that automatically **extends the lifespan of a record** when it is accessed or updated. This ensures that frequently used records remain in the cache while inactive records expire naturally.

### How Does It Work?
- When you **get** a record, its TTL is reset, so it stays in the cache as long as it is actively accessed.
- When you **update** a record, its TTL is also refreshed to ensure it doesn’t expire while still in use.
- The library maintains a **separate tracking mechanism** to efficiently update TTL without modifying the full record.

### Example Usage
```python
# Enable Active TTL when initializing the cache
cache = RedisCache()

# Set a record with Active TTL enabled
cache["session:456"] = {"user": "Alice", "status": "active"}

# Accessing the record within the TTL period will extend its TTL
user_session = cache["session:456"]
print(user_session)  # {'user': 'Alice', 'status': 'active'}
```

### Why Use Active TTL?
✅ **Prevents unnecessary cache evictions for frequently used data**
✅ **Ensures session-like behavior (e.g., user sessions, API response caching, temporary data)**
✅ **Users don't need to manually manage TTL; it is handled automatically**
✅ **Set TTL once, and Active TTL will extend it dynamically based on access**

## How to Enable Active TTL
### Enabling Active TTL
Active TTL is enabled by default, but you can explicitly configure it using environment variables.
```sh
export REDIS_ACTIVE_TTL=true  # Enables Active TTL
export REDIS_DEFAULT_TTL=3600  # Default TTL in seconds (1 hour)
```

### Example Usage
```python
# Enable Active TTL with default TTL
cache = RedisCache()
cache["user:session"] = {"id": 123, "status": "active"}
print(cache["user:session"])  # Output: {'id': 123, 'status': 'active'}
```

## Lazy Cleanup Mechanism
### What is Lazy Cleanup?
Lazy cleanup ensures that expired or inactive records are removed in an efficient manner without causing unnecessary Redis load. Instead of continuously checking and deleting expired keys, the cleanup process runs periodically, removing only stale entries.

### Example Usage
```python
# Run cleanup to remove inactive records older than 60 minutes
cache.cleanup_inactive_records(past_minutes=60)
```

## Configuration
You can configure Redis settings using environment variables:
```sh
export REDIS_HOST=localhost
export REDIS_PORT=6379
export REDIS_DB=0
export REDIS_PASSWORD=yourpassword
export REDIS_DEFAULT_TTL=3600
export REDIS_ACTIVE_TTL=true
```

## Developer Guide
### Setting Up for Development
To modify and test this library, follow these steps:
```sh
# Clone the repository
git clone https://github.com/yourusername/rcache-live.git
cd rcache-live

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt
```

### Running Tests
Since test cases are not included in the repo, developers should create their own `tests/` folder and include the following test cases:
```python
import pytest
import time
from rcache_live.redis_cache import RedisCache

@pytest.fixture
def cache():
    return RedisCache(active_ttl=True)

def test_set_and_get_record(cache):
    cache["test_key"] = {"name": "Alice"}
    assert cache["test_key"] == {"name": "Alice"}

def test_update_record(cache):
    cache["test_key"] = {"name": "Alice"}
    cache.update("test_key", age=30)
    assert cache["test_key"] == {"name": "Alice", "age": 30}

def test_bulk_set_and_delete(cache):
    cache.add(user1={"name": "Alice"}, user2={"name": "Bob"})
    assert cache["user1"] == {"name": "Alice"}
    assert cache["user2"] == {"name": "Bob"}
    cache.bulk_delete(["user1", "user2"])
    assert cache.get_record("user1") is None
    assert cache.get_record("user2") is None
```
To run the tests:
```sh
pytest tests/
```

## Configuration
You can configure Redis settings using environment variables:
```sh
export REDIS_HOST=localhost
export REDIS_PORT=6379
export REDIS_DB=0
export REDIS_PASSWORD=yourpassword
export REDIS_DEFAULT_TTL=3600
export REDIS_ACTIVE_TTL=true
```

## Contributing
Contributions are welcome! Feel free to open issues or submit pull requests.

## License
This project is licensed under the MIT License.