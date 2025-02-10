from rcache_live import RCacheLive
import time

# Initialize cache with Active TTL enabled
cache = RCacheLive(active_ttl=True)

print("\n✅ Setting a record...")
cache["user:123"] = {"name": "Alice", "age": 25}
print("Stored:", cache["user:123"])  # Should print {'name': 'Alice', 'age': 25}

print("\n✅ Updating a specific field...")
cache.update("user:123", age=26)  # Only update 'age'
print("After age update:", cache["user:123"])  # Should print {'name': 'Alice', 'age': 26}

print("\n✅ Updating entire record...")
cache["user:123"] = {"name": "Alice Smith", "age": 27, "city": "New York"}
print("After full update:", cache["user:123"])  # Should print updated record

print("\n✅ Bulk inserting multiple records...")
cache.add(user1={"name": "Bob"}, user2={"name": "Charlie", "age": 30})
print("User1:", cache["user1"])  # Should print {'name': 'Bob'}
print("User2:", cache["user2"])  # Should print {'name': 'Charlie', 'age': 30}

print("\n✅ Retrieving all records...")
all_records = cache.get_all_records()
print("All stored records:", all_records)

print("\n✅ Demonstrating Active TTL...")
cache["session:456"] = {"user": "Alice", "status": "active"}
print("Before access:", cache["session:456"])
time.sleep(3)  # Simulate waiting
print("After access:", cache["session:456"])  # Access resets TTL

print("\n✅ Deleting a record...")
cache.delete_record("user:123")
print("Deleted user:123, now:", cache.get_record("user:123"))  # Should be None

print("\n✅ Bulk deleting records...")
cache.bulk_delete(["user1", "user2"])
print("Deleted user1:", cache.get_record("user1"))  # Should be None
print("Deleted user2:", cache.get_record("user2"))  # Should be None

print("\n✅ Testing Lazy Cleanup...")
cache["old_key"] = {"data": "old"}
print("Before cleanup:", cache["old_key"])
time.sleep(7)  # Simulating old key expiration
cache.cleanup_inactive_records(past_minutes=0.1)
print("After cleanup:", cache.get_record("old_key"))  # Should be None

print("\n🎉 All operations completed successfully!")