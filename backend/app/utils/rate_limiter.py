from app.utils.redis_client import redis_client

MAX_REQUESTS = 5
WINDOW_SECONDS = 60

def check_rate_limit(client_ip):
    key = f"rate:{client_ip}"
    current_count = redis_client.incr(key)

    if current_count == 1:
        redis_client.expire(key,WINDOW_SECONDS)

    if current_count > MAX_REQUESTS:
        remaining_time = redis_client.ttl(key)
        return False, remaining_time
    return True, 0