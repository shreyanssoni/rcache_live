# Redis Cache Library

[![PyPI version](https://badge.fury.io/py/rcache-live.svg)](https://pypi.org/project/rcache-live/)

## Overview
This is a simple and efficient Redis caching library for Python that supports **Active TTL**. It provides an easy-to-use interface for storing, retrieving, and managing cached data while automatically refreshing TTL for active records (if enabled). The library is designed for caching any type of data, not just user sessions, making it a versatile solution for various use cases.

## Features
- **Dictionary-style access** (`cache[key] = value` and `cache[key]`)
- **Auto field updates** via `update()`
- **Bulk insert shortcut** via `add()`
- **Configurable Redis Credentials** via `config.py`
- **Custom TTL per Record** (default and per-key support)
- **Optional Active TTL** (Resets TTL when a record is accessed or updated if enabled)
- **Efficient Background Cleanup** for stale records
- **Simple API for CRUD Operations**

## Installation
```sh
pip install rcache-live
```

## Usage

### Initialize the Cache
```python
from rcache_live.rcache_handler import RCacheLive

# Create a Redis cache instance (Active TTL is disabled by default)
cache = RCacheLive()

# Create a Redis cache instance with Active TTL enabled
cache = RCacheLive(active_ttl=True)
```

### Set and Get a Record (Dictionary-Style Access)
```python
cache["test_key"] = {"name": "Alice"}  # Set a record
print(cache["test_key"])  # Get a record
```

### Auto Field Updates
```python
cache["test_key"] = {"name": "Alice", "age": 25}
cache.update("test_key", age=26)
print(cache["test_key"])  # Output: {'name': 'Alice', 'age': 26}
```

### Bulk Insert Shortcut
```python
cache.add(key1={"data": 1}, key2={"data": 2})
print(cache["key1"])  # Output: {'data': 1}
print(cache["key2"])  # Output: {'data': 2}
```

### Delete a Record
```python
cache.delete_record("test_key")
print(cache.get_record("test_key"))  # Output: None
```

### Get All Records
```python
all_records = cache.get_all_records()
print(all_records)
```

### Cleanup Inactive Records
```python
cache.cleanup_inactive_records(past_minutes=0.1)
```

## Active TTL - Unique Feature (Optional)
### What is Active TTL?
Active TTL is a feature that **automatically extends the lifespan of a record** when it is accessed or updated. This ensures that frequently used records remain in the cache while inactive records expire naturally.

### How Does It Work?
- When you **get** a record, its TTL is reset (only if `active_ttl=True`).
- When you **update** a record, its TTL is also refreshed.
- The library maintains a **separate tracking mechanism** to efficiently update TTL without modifying the full record.

### Example Usage
```python
# Enable Active TTL when initializing the cache
cache = RCacheLive(active_ttl=True)

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

## Lazy Cleanup Mechanism
### What is Lazy Cleanup?
Lazy cleanup ensures that expired or inactive records are removed in an efficient manner without causing unnecessary Redis load.

### Example Usage
```python
# Run cleanup to remove inactive records older than 6 seconds
cache.cleanup_inactive_records(past_minutes=0.1)
```

## Developer Guide
### Running Tests
The test cases are included in the repo, developers should run the tests before raising a new pull request
```
To run the tests:
```sh
pytest tests/
```

## License
This project is licensed under the MIT License.
