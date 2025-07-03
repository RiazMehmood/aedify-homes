from fastapi import Request, HTTPException
from jose import jwt, JWTError
import os

SECRET_KEY = os.getenv("NEXTAUTH_SECRET")
ALGORITHM = "HS256"

async def get_current_user(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")

    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {
            "email": payload.get("email"),
            "id": payload.get("sub") or payload.get("email"),
        }
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
