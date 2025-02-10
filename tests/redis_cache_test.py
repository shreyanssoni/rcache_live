import pytest
import time
import sys
import os

# Ensure the parent directory is in the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from rcache_live import RCacheLive

@pytest.fixture
def cache():
    return RCacheLive(active_ttl=True)

def test_set_and_get_record(cache):
    cache["test_key"] = {"name": "Alice"}
    assert cache["test_key"] == {"name": "Alice"}

def test_update_record(cache):
    cache["test_key"] = {"name": "Alice"}
    cache.update("test_key", name="Bob")
    assert cache["test_key"] == {"name": "Bob"}

def test_update_record_field(cache):
    cache["test_key"] = {"name": "Alice", "age": 25}
    cache.update("test_key", age=26)
    assert cache["test_key"] == {"name": "Alice", "age": 26}

def test_delete_record(cache):
    cache["test_key"] = {"name": "Alice"}
    cache.delete_record("test_key")
    assert cache.get_record("test_key") is None

def test_active_ttl(cache):
    cache["test_key"] = {"name": "Alice"}
    time.sleep(3)
    cache.get_record("test_key")  # Access should reset TTL
    time.sleep(3)
    assert cache.get_record("test_key") == {"name": "Alice"}  # Should still exist

def test_bulk_set_and_delete(cache):
    cache.add(key1={"data": 1}, key2={"data": 2})
    assert cache["key1"] == {"data": 1}
    assert cache["key2"] == {"data": 2}
    cache.bulk_delete(["key1", "key2"])
    assert cache.get_record("key1") is None
    assert cache.get_record("key2") is None

def test_lazy_cleanup(cache):
    cache["old_key"] = {"data": "old"}
    assert cache.get_record("old_key") is not None  # Ensure it's set
    print("Sleeping to let key expire...")
    time.sleep(7)  # Wait 7 seconds (longer than 6 seconds)
    cache.cleanup_inactive_records(past_minutes=0.1)
    print("Checking if key still exists...")
    assert cache.get_record("old_key") is None  # Now it should be deleted

def test_get_nonexistent_record(cache):
    """Test getting a record that doesn't exist."""
    try:
        assert cache.get_record("nonexistent_key") is None
    except Exception as e:
        handle_error("test_get_nonexistent_record", e)

def test_delete_nonexistent_record(cache):
    """Test deleting a nonexistent record (should not raise an error)."""
    try:
        cache.delete_record("nonexistent_key")  # Shouldn't break anything
        assert cache.get_record("nonexistent_key") is None
    except Exception as e:
        handle_error("test_delete_nonexistent_record", e)

def test_invalid_update(cache):
    """Test updating a record that doesn't exist."""
    try:
        cache.update("invalid_key", age=30)  # Should create the record
        assert cache["invalid_key"] == {"age": 30}
    except Exception as e:
        handle_error("test_invalid_update", e)