from app.utils.redis_client import redis_client

MAX_REQUESTS = 5
WINDOW_SECONDS = 60

def check_rate_limit(client_ip):
    key = f"rate:{client_ip}"
    current_count = redis_client.get(key)
    if current_count is None:
        redis_client.set(key, 1, ex=WINDOW_SECONDS)
        return True
    current_count = int(current_count)
    if current_count >= MAX_REQUESTS:
        return False
    redis_client.incr(key)
    return True