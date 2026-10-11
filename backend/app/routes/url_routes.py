from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import RedirectResponse
from app.controllers.url_controller import create_short_url, find_short_url, get_url_details, remove_url, edit_url
from app.models.url_model import URLCreate
from app.utils.redis_client import redis_client
from app.utils.rate_limiter import check_rate_limit
from app.utils.auth import get_current_user

router = APIRouter()

@router.post("/api/urls")
def create_url(request: Request, url: URLCreate, user_id: int = Depends(get_current_user)):
    client_ip = request.client.host
    allowed, retry_after = check_rate_limit(client_ip)
    if not allowed:
        raise HTTPException (
            status_code=429,
            detail="Rate limit exceeded",
            headers={
                "Retry-After": str(retry_after)
            }
        )
    return create_short_url(url, user_id)

@router.get("/api/urls/{short_code}")
def get_url(short_code: str, user_id: int = Depends(get_current_user)):
    result = get_url_details(short_code, user_id)
    if result is None:
        return{"message": "Short URL not found"}
    return result

@router.get("/{short_code}")
def redirect_url(short_code: str):
    result = find_short_url(short_code)
    if result is None:
        raise HTTPException(
                status_code = 401,
                detail = "URL not found"
            )
    original_url = result
    return RedirectResponse(url = original_url, status_code=302)

@router.delete("/api/urls/{short_code}")
def delete_short_url(short_code: str, user_id: int = Depends(get_current_user)):
    result = remove_url(short_code, user_id)
    if result is None:
        raise HTTPException(
            status_code = 401,
            detail = "URL not found"
        )
    return result

@router.put("/api/urls/{short_code}")
def update_short_url(short_code: str, url: URLCreate, user_id: int = Depends(get_current_user)):
    result = edit_url(short_code, url.original_url, user_id)
    if result is None:
        return {"message": "Short URL not found"}
    return result

@router.get("/api/test-redis")
def test_redis():
    redis_client.set("test_key", "hello redis")
    value = redis_client.get("test_key")
    return {"message": value}

@router.get("/api/test-rate-limiter")
def test_rate_limit(request: Request):
    client_ip = request.client.host
    allowed = check_rate_limit(client_ip)
    if not allowed:
        return {
            "message": "Rate limit exceeded",
            "ip": client_ip
        }
    return {
        "message": "Request allowed",
        "ip": client_ip
    }