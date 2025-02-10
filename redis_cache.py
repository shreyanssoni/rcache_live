import redis
import json
import time
from rcache_live.config import RedisConfig
from rcache_live.utils import serialize, deserialize, current_timestamp

class RedisCache:
    def __init__(self, host='localhost', port=6379, db=0, password=None, default_ttl=3600, active_ttl=False):
        """
        Initialize Redis Cache with connection settings.
        :param host: Redis host
        :param port: Redis port
        :param db: Redis database index
        :param password: Redis password
        :param default_ttl: Default TTL for keys (in seconds)
        :param active_ttl: If True, TTL resets on update or access
        """
        self.client = redis.Redis(host=host, port=port, db=db, password=password, decode_responses=True)
        self.default_ttl = default_ttl
        self.active_ttl = active_ttl  # Store the flag

    def set_record(self, key, value, ttl=None):
        """Set a record and track last_access separately."""
        ttl = ttl or self.default_ttl
        self.client.setex(key, ttl, serialize(value))  # Store main data
        if self.active_ttl:
            self.client.hset("active_ttl_tracker", key, current_timestamp())  # Store last_access separately

    def get_record(self, key):
        """Get a record and update last_access timestamp separately."""
        value = self.client.get(key)
        if value and self.active_ttl:
            self.client.hset("active_ttl_tracker", key, current_timestamp())  # Update last access
            self.client.expire(key, self.default_ttl)  # Reset TTL
        return deserialize(value) if value else None

    def update_record(self, key, new_value):
        """Update an entire record, resetting TTL and last_access timestamp if active_ttl is enabled."""
        if self.client.exists(key):
            self.set_record(key, new_value)
            return True
        return False

    def update_record_field(self, key, field, value):
        """Update a single field in a JSON record, resetting TTL if active_ttl is enabled."""
        record = self.get_record(key)
        if record:
            record[field] = value
            self.set_record(key, record)
            return True
        return False

    def delete_record(self, key):
        """Delete a record and remove it from the active TTL tracker."""
        self.client.delete(key)
        if self.active_ttl:
            self.client.hdel("active_ttl_tracker", key)

    def get_all_records(self, pattern="*"):
        """Get all records matching a pattern."""
        keys = self.client.keys(pattern)
        return {key: self.get_record(key) for key in keys}

    def cleanup_inactive_records(self, past_minutes=60):
        """Background job: Delete records that haven’t been accessed in past X minutes."""
        now = current_timestamp()
        min_time = now - (past_minutes * 60)
        keys = self.client.hgetall("active_ttl_tracker")  # Get all tracked access times
        for key, last_access in keys.items():
            if int(last_access) < min_time:
                self.client.delete(key)  # Delete stale record
                self.client.hdel("active_ttl_tracker", key)  # Remove from tracking

    def bulk_set(self, records):
        """Set multiple records at once."""
        with self.client.pipeline() as pipe:
            for key, value in records.items():
                pipe.setex(key, self.default_ttl, serialize(value))
                if self.active_ttl:
                    pipe.hset("active_ttl_tracker", key, current_timestamp())
            pipe.execute()

    def bulk_delete(self, keys):
        """Delete multiple records at once and remove from active TTL tracking."""
        self.client.delete(*keys)
        if self.active_ttl:
            self.client.hdel("active_ttl_tracker", *keys)