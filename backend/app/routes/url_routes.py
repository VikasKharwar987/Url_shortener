from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from app.controllers.url_controller import create_short_url, find_short_url, get_url_details, remove_url, edit_url
from app.models.url_model import URLCreate
from app.utils.redis_client import redis_client

router = APIRouter()

@router.post("/api/urls")
def create_url(url: URLCreate):
    return create_short_url(url)

@router.get("/api/urls/{short_code}")
def get_url(short_code: str):
    result = get_url_details(short_code)
    if result is None:
        return{"message": "Short URL not found"}
    return result

@router.get("/{short_code}")
def redirect_url(short_code: str):
    result = find_short_url(short_code)
    if result is None:
        return {"message": "Short url not found"}
    original_url = result
    return RedirectResponse(url = original_url, status_code=302)

@router.delete("/api/urls/{short_code}")
def delete_short_url(short_code: str):
    result = remove_url(short_code)
    if result is None:
        return{"message": "Short URL not found"}
    return result

@router.put("/api/urls/{short_code}")
def update_short_url(short_code: str, url: URLCreate):
    result = edit_url(short_code, url.original_url)
    if result is None:
        return {"message": "Short URL not found"}
    return result

@router.get("/api/test-redis")
def test_redis():
    redis_client.set("test_key", "hello redis")
    value = redis_client.get("test_key")
    return {"message": value}