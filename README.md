# Redis Cache Library

## Overview
This is a simple and efficient Redis caching library for Python that supports **Active TTL**. It provides an easy-to-use interface for storing, retrieving, and managing cached data while automatically refreshing TTL for active records. The library is designed for caching any type of data, not just user sessions, making it a versatile solution for various use cases.
This is a simple and efficient Redis caching library for Python that supports **Active TTL**. It provides an easy-to-use interface for storing, retrieving, and managing cached data while automatically refreshing TTL for active records.

## Features
- **Configurable Redis Credentials** via `config.py`
- **Custom TTL per Record** (default and per-key support)
- **Active TTL** (Resets TTL when a record is accessed or updated)
- **Efficient Background Cleanup** for stale records
- **Simple API for CRUD Operations**
- **Batch Operations** (Bulk set and delete)

## Installation
```sh
pip install redis-cache-lib
```

## Usage

### Initialize the Cache
```python
from redis_cache import RedisCache

# Create a Redis cache instance
cache = RedisCache()
```

### Set a Record
```python
cache.set_record("user:123", {"name": "John Doe", "age": 30}, ttl=3600)
```

### Get a Record
```python
user = cache.get_record("user:123")
print(user)  # Output: {'name': 'John Doe', 'age': 30}
```

### Update a Record
```python
cache.update_record("user:123", {"name": "John Doe", "age": 31})
```

### Update a Specific Field in a Record
```python
cache.update_record_field("user:123", "age", 32)
```

### Delete a Record
```python
cache.delete_record("user:123")
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
This caching mechanism is designed to work with any data type, including user sessions, API responses, temporary data storage, and more.
```python
# Enable Active TTL when initializing the cache
cache = RedisCache()

# Set a record with Active TTL enabled
cache.set_record("session:456", {"user": "Alice", "status": "active"}, ttl=300)  # 5 min TTL

# Accessing the record within 5 minutes will extend its TTL
user_session = cache.get_record("session:456")
print(user_session)  # {'user': 'Alice', 'status': 'active'}

# The record remains in cache as long as it is accessed frequently
```

### Why Use Active TTL?
✅ **Works for all data types**
✅ **Prevents unnecessary cache evictions for frequently used data**
✅ **Ensures session-like behavior (e.g., user sessions, API response caching, temporary data)**
✅ **Users don't need to manually manage TTL; it is handled automatically**
✅ **Set TTL once, and Active TTL will extend it dynamically based on access**
✅ **Prevents unnecessary cache evictions for frequently used data**
✅ **Ensures session-like behavior (e.g., user sessions, authentication tokens)**
✅ **Users don't need to manually manage TTL; it is handled automatically**
✅ **Set TTL once, and Active TTL will extend it dynamically based on access**

**Example:**
```python
# Set a record with a 10-minute TTL
cache.set_record("cart:789", {"items": ["apple", "banana"]}, ttl=600)

# Accessing it within 10 minutes will keep it alive
cart_data = cache.get_record("cart:789")
print(cart_data)  # {'items': ['apple', 'banana']}

# As long as it's accessed, it will never expire prematurely
```

## How to Enable Active TTL
### Enabling Active TTL
Active TTL is enabled by default, but you can explicitly configure it using environment variables. Set `REDIS_ACTIVE_TTL=true` to ensure records dynamically extend their TTL upon access or update.

### Required Configuration Values
```sh
export REDIS_ACTIVE_TTL=true  # Enables Active TTL
export REDIS_DEFAULT_TTL=3600  # Default TTL in seconds (1 hour)
```

### Example Usage
```python
# Enable Active TTL with default TTL
cache = RedisCache()

# Store a record with a TTL of 5 minutes
cache.set_record("user:session", {"id": 123, "status": "active"}, ttl=300)

# Accessing the record resets TTL, keeping it in cache
print(cache.get_record("user:session"))
```

## Using TTL Without Active TTL
If you want records to expire after a set duration without automatic renewal, disable Active TTL:
```sh
export REDIS_ACTIVE_TTL=false
```
This means records will expire exactly after the specified TTL, even if accessed frequently.

## Lazy Cleanup Mechanism
### What is Lazy Cleanup?
Lazy cleanup ensures that expired or inactive records are removed in an efficient manner without causing unnecessary Redis load. Instead of continuously checking and deleting expired keys, the cleanup process runs periodically, removing only stale entries.

### How Does It Work?
- A background process runs at scheduled intervals to clean up inactive records.
- Instead of relying solely on Redis's built-in expiration, the cache checks when records were last accessed and removes them if they exceed the set threshold.
- This mechanism ensures that expired records do not clutter the database, improving performance.

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

## Contributing
Contributions are welcome! Feel free to open issues or submit pull requests.

## License
This project is licensed under the MIT License.

