from typing import Optional, List
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
    subscription: Optional[str] = None
    subscription_details: Optional[dict] = None
    subscription_expiry: Optional[str] = None


# ========== Property Detail Schemas ==========

class ResidentialSellDetails(BaseModel):
    price: float
    negotiable: bool
    address: str
    bedrooms: int
    bathrooms: int
    floor_number: Optional[str] = None
    total_area_yards: float
    documents: str  # "documented" or "kacha"
    description: Optional[str] = ""

class ResidentialRentDetails(BaseModel):
    monthly_rent: float
    negotiable: bool
    advance_amount: float
    utility_bills_included: bool
    address: str
    bedrooms: int
    bathrooms: int
    floor_number: Optional[str] = None
    total_area_yards: Optional[float] = None
    description: Optional[str] = ""

class CommercialRentDetails(BaseModel):
    monthly_rent: float
    negotiable: bool
    advance_amount: float
    utility_bills_included: bool
    address: str
    area_yards: float
    floor_number: Optional[str] = None
    description: Optional[str] = ""

class CommercialSellDetails(BaseModel):
    price: float
    negotiable: bool
    address: str
    area_yards: float
    floor_number: Optional[str] = None
    description: Optional[str] = ""

class AgriculturalLeaseDetails(BaseModel):
    rent_per_acre: float
    negotiable: bool
    address: str
    total_area: float
    lease_duration: int
    available_area: float
    description: Optional[str] = ""

class AgriculturalSellDetails(BaseModel):
    price_per_acre: float
    negotiable: bool
    address: str
    total_area: float
    available_area: float
    description: Optional[str] = ""

# ========== Main Property Model ==========

class PropertyInput(BaseModel):
    category: str  # "residential", "commercial", "agricultural"
    subcategory: str  # "rent", "sell", "lease"
    title: str
    images: List[str] = []

    # Optional Details for Conditional Fields
    residential_sell: Optional[ResidentialSellDetails] = None
    residential_rent: Optional[ResidentialRentDetails] = None
    commercial_rent: Optional[CommercialRentDetails] = None
    commercial_sell: Optional[CommercialSellDetails] = None
    agricultural_lease: Optional[AgriculturalLeaseDetails] = None
    agricultural_sell: Optional[AgriculturalSellDetails] = None


class RealEstateInput(BaseModel):
    is_real_estate_query: bool
    query: str

class Input(BaseModel):
    value: str