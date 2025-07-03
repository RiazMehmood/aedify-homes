from pydantic import BaseModel

class PropertyModerationInput(BaseModel):
    property_id: str
    category: str
    city: str
    created_at: str
    description: str
    status: str
    review_comment: str
    subcategory: str
    images: list[str]
    title: str
    email: str

class PropertyModerationOutput(BaseModel):
    status: str
    review_comment: str
    property_id: str

class UserInfo(BaseModel):
    name: str
    city: str
    role: str
    whatsapp: int | str | None = None
