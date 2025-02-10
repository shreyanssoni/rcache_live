import redis
import json
import time
from rcache_live.config import RedisConfig
from rcache_live.utils import serialize, deserialize, current_timestamp
from rcache_live.error_handler import handle_error

class RCacheLive:
    def __init__(self, host='localhost', port=6379, db=0, password=None, default_ttl=3600, active_ttl=False):
        """
        Initialize Redis Cache with connection settings.
        """
        try:
            self.client = redis.Redis(host=host, port=port, db=db, password=password, decode_responses=True)
            self.default_ttl = default_ttl
            self.active_ttl = active_ttl  # Store the flag
        except Exception as e:
            handle_error("__init__", e)

    def __setitem__(self, key, value):
        """Set a record using dictionary-style access."""
        try:
            self.set_record(key, value)
        except Exception as e:
            handle_error("__setitem__", e)

    def __getitem__(self, key):
        """Get a record using dictionary-style access."""
        try:
            return self.get_record(key)
        except Exception as e:
            handle_error("__getitem__", e)
            return None

    def set_record(self, key, value, ttl=None):
        """Set a record and track last_access separately."""
        try:
            ttl = ttl or self.default_ttl
            self.client.setex(key, ttl, serialize(value))
            if self.active_ttl:
                self.client.hset("active_ttl_tracker", key, current_timestamp())
        except Exception as e:
            handle_error("set_record", e)

    def get_record(self, key):
        """Get a record and update last_access timestamp separately."""
        try:
            value = self.client.get(key)
            if value and self.active_ttl:
                self.client.hset("active_ttl_tracker", key, current_timestamp())
                self.client.expire(key, self.default_ttl)
            return deserialize(value) if value else None
        except Exception as e:
            handle_error("get_record", e)
            return None

    def update(self, key, **kwargs):
        """Update specific fields of a record instead of replacing the entire record."""
        try:
            record = self.get_record(key) or {}
            record.update(kwargs)
            self.set_record(key, record)
            return True
        except Exception as e:
            handle_error("update", e)
            return False

    def delete_record(self, key):
        """Delete a record and remove it from the active TTL tracker."""
        try:
            self.client.delete(key)
            if self.active_ttl:
                self.client.hdel("active_ttl_tracker", key)
        except Exception as e:
            handle_error("delete_record", e)

    def get_all_records(self, pattern="*"):
        """Get all records matching a pattern, excluding 'active_ttl_tracker'."""
        try:
            keys = self.client.keys(pattern)
            print("Keys:", keys)

            return {
                str(key): self.get_record(str(key))
                for key in keys
                if key != "active_ttl_tracker"
            }
        except Exception as e:
            handle_error("get_all_records", e)
            return {}

    def cleanup_inactive_records(self, past_minutes=60):
        """Background job: Delete records that haven't been accessed in past X minutes."""
        try:
            now = current_timestamp()
            min_time = now - (past_minutes * 60)
            keys = self.client.hgetall("active_ttl_tracker")  # Get all tracked access times

            for key, last_access in keys.items():
                last_access_time = int(last_access)
                if last_access_time < min_time:
                    print(f"Deleting {key} due to inactivity")
                    self.client.delete(key)  # Delete stale record
                    self.client.hdel("active_ttl_tracker", key)  # Remove from tracking
        except Exception as e:
            handle_error("cleanup_inactive_records", e)

    def add(self, **kwargs):
        """Set multiple records at once using keyword arguments."""
        try:
            for key, value in kwargs.items():
                self.set_record(key, value)
        except Exception as e:
            handle_error("add", e)

    def bulk_delete(self, keys):
        """Delete multiple records at once and remove from active TTL tracking."""
        try:
            self.client.delete(*keys)
            if self.active_ttl:
                self.client.hdel("active_ttl_tracker", *keys)
        except Exception as e:
            handle_error("bulk_delete", e)
