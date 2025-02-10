import os

class RedisConfig:
    """Handles Redis configuration using environment variables or defaults."""
    
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
    REDIS_DB = int(os.getenv("REDIS_DB", 0))
    REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)
    DEFAULT_TTL = int(os.getenv("REDIS_DEFAULT_TTL", 3600))  # Default TTL in seconds
    ACTIVE_TTL = os.getenv("REDIS_ACTIVE_TTL", "false").lower() == "true"  # Convert to boolean

    @classmethod
    def get_config(cls):
        """Returns Redis configuration as a dictionary."""
        return {
            "host": cls.REDIS_HOST,
            "port": cls.REDIS_PORT,
            "db": cls.REDIS_DB,
            "password": cls.REDIS_PASSWORD,
            "default_ttl": cls.DEFAULT_TTL,
            "active_ttl": cls.ACTIVE_TTL,
        }
