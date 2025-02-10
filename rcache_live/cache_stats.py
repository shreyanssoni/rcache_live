import redis
from rcache_live.config import RedisConfig

def get_cache_stats():
    """Fetch and display Redis cache statistics."""
    client = redis.Redis(
        host=RedisConfig.REDIS_HOST, 
        port=RedisConfig.REDIS_PORT, 
        db=RedisConfig.REDIS_DB, 
        password=RedisConfig.REDIS_PASSWORD, 
        decode_responses=True
    )

    try:
        info = client.info()  # Get Redis stats
        keys = client.keys("*")  # Get all keys
        active_ttl_keys = client.hkeys("active_ttl_tracker")  # Keys with active TTL

        stats = {
            "Total Keys": len(keys),
            "Keys with Active TTL": len(active_ttl_keys),
            "Memory Used (MB)": round(info.get("used_memory", 0) / 1024 / 1024, 2),
            "Cache Hits": info.get("keyspace_hits", 0),
            "Cache Misses": info.get("keyspace_misses", 0),
            "Hit Ratio": f"{round((info.get('keyspace_hits', 0) / max(1, (info.get('keyspace_hits', 0) + info.get('keyspace_misses', 0)))) * 100, 2)}%"
        }

        print("\n📊 RCache-Live Statistics 📊")
        print("=" * 30)
        for key, value in stats.items():
            print(f"- {key}: {value}")

    except Exception as e:
        print("Error fetching Redis stats:", e)

if __name__ == "__main__":
    get_cache_stats()
