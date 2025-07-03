from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from utils.azure_blob import upload_image_to_blob
from routes.auth import get_current_user

router = APIRouter()

@router.post("/api/upload")
async def upload_image(file: UploadFile = File(...), user: dict = Depends(get_current_user)):
    if user.get("role") != "seller":
        raise HTTPException(status_code=403, detail="Only sellers can upload images.")

    image_url = await upload_image_to_blob(file)
    return {"url": image_url}
