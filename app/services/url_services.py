import string
import random
from app.db.redis_client import redis_client

def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def create_short_url(original_url: str):
    short_code = generate_short_code()

    while redis_client.exists(short_code):
        short_code = generate_short_code()

    redis_client.set(short_code, original_url)
    return short_code

def get_original_url(short_code: str):
    return redis_client.get(short_code)