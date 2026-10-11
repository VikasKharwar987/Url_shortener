import jwt
from datetime import datetime, timedelta, timezone

from app.utils.jwt_handler import (
    create_access_token,
    JWT_SECRET,
    JWT_ALGORITHM
)
from app.utils.auth import get_current_user


# Test 1: Valid token
token = create_access_token(user_id=1)
user_id = get_current_user(token)

print("Valid token user ID:", user_id)
assert user_id == 1


# Test 2: Invalid token
try:
    get_current_user("this.is.invalid")
    assert False, "Invalid token should be rejected"
except Exception as error:
    print("Invalid token rejected:", error.status_code)


# Test 3: Expired token
expired_payload = {
    "sub": "1",
    "exp": datetime.now(timezone.utc) - timedelta(minutes=1)
}

expired_token = jwt.encode(
    expired_payload,
    JWT_SECRET,
    algorithm=JWT_ALGORITHM
)

try:
    get_current_user(expired_token)
    assert False, "Expired token should be rejected"
except Exception as error:
    print("Expired token rejected:", error.status_code)


print("All JWT verification tests passed!")