from fastapi import Request, HTTPException, Depends
from jose import JWTError, jwt
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from db.mongo import users_collection
from passlib.context import CryptContext
import os


class OnboardingDetails(BaseModel):
    phone: str
    whatsapp: str
    email: EmailStr
    cnic: str
    city: str
    role: str

class UserSignup(BaseModel):
    name: str
    email: EmailStr
    password: str

class SessionCreate(BaseModel):
    email: EmailStr
    user_agent: str
    ip: str

class UserSignin(BaseModel):
    email: EmailStr
    password: str


router = APIRouter()
@router.post("/onboarding")
async def onboarding_user(details: OnboardingDetails):
    result = users_collection.update_one(
        {"email": details.email},
        {
            "$set": {
                "phone": details.phone,
                "whatsapp": details.whatsapp,
                "cnic": details.cnic,
                "city": details.city,
                "role": details.role,
                "onboarding_complete": True
            }
        }
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "Onboarding complete"}


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/signup")
async def signup_user(user: UserSignup):
    existing_user = users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_pw = pwd_context.hash(user.password)
    new_user = {
        "name": user.name,
        "email": user.email,
        "password": hashed_pw,
        "auth_provider": "email"
    }
    users_collection.insert_one(new_user)
    return {"message": "User created successfully", "onboarding_required": True}


@router.post("/signin")
async def signin_user(user: UserSignin):
    existing_user = users_collection.find_one({"email": user.email})
    if not existing_user or not pwd_context.verify(user.password, existing_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return {
        "message": "Login successful",
        "email": existing_user["email"],
        "name": existing_user.get("name", ""),
        "onboarding_complete": existing_user.get("onboarding_complete", False)
    }

@router.post("/check-user")
async def check_user_exists(payload: dict):
    email = payload.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Email is required")

    user = users_collection.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "onboarding_complete": user.get("onboarding_complete", False),
        "role": user.get("role", "customer")
    }

@router.post("/google")
async def google_login(user: dict):
    email = user.get("email")
    name = user.get("name")

    if not email:
        raise HTTPException(status_code=400, detail="Missing email from Google")

    existing_user = users_collection.find_one({"email": email})

    if not existing_user:
        # Create user entry
        users_collection.insert_one({
            "email": email,
            "name": name,
            "auth_provider": "google",
            "onboarding_complete": False
        })

    return {"message": "User checked/created successfully"}


SECRET_KEY = os.getenv("NEXTAUTH_SECRET")  # Same key from .env
ALGORITHM = "HS256"  # NextAuth default

async def get_current_user(request: Request):
    auth_header = request.headers.get("Authorization")
    print("Authorization header:", auth_header)
    print("Authorization header (raw):", auth_header)
    if not auth_header or not auth_header.startswith("Bearer "):
        print("Request headers:", dict(request.headers))
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
    token = auth_header.split(" ")[1]

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        print("Decoded JWT payload:", payload)

        email = payload.get("email")
        if not email:
            raise HTTPException(status_code=401, detail="Token missing email")

        # Now fetch user from MongoDB
        user = users_collection.find_one({"email": email})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user

    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid token")
