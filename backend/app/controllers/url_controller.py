from app.models.url_model import create_url, get_test_url, get_url_by_short_code, increment_click_count, delete_url, update_url
from app.utils.redis_client import redis_client

def create_short_url(url):
    result = create_url(url.original_url)
    if result is None:
        return {"message": "No URL found"}
    return {
        "id": result[0],
        "short_code": result[1],
        "original_url": result[2],
        "click_count": result[3]
    }

def find_short_url(short_code):
    cache_key = f"url:{short_code}"
    cached_url = redis_client.get(cache_key)
    if cached_url:
        print("CACHE HIT")
        increment_click_count(short_code)
        return cached_url
    print("CACHE MISS")
    result = get_url_by_short_code(short_code)
    if result is None:
        return None
    original_url = result[2]
    redis_client.set(cache_key, original_url)
    increment_click_count(short_code)
    return original_url

def get_url_details(short_code):
    result = get_url_by_short_code(short_code)
    if result is None:
        return None
    return {
        "id": result[0],
        "short_code": result[1],
        "original_url": result[2],
        "click_count": result[3]
    }

def remove_url(short_code):
    deleted_rows = delete_url(short_code)
    if deleted_rows == 0:
        return None
    cache_key = f"url:{short_code}"
    redis_client.delete(cache_key)
    return{
        "message": "Short URL deleted successfully",
        "short_code": short_code
    }

def edit_url(short_code, original_url):
    updated_rows = update_url(short_code, original_url)
    if updated_rows == 0:
        return None
    cache_key = f"url:{short_code}"
    redis_client.delete(cache_key)
    return {
        "message": "Short URL updated successfully",
        "short_code": short_code,
        "original_url": str(original_url)
    }