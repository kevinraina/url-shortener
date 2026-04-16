import os

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
