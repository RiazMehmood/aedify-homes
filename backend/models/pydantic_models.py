from typing import Optional, List
from pydantic import BaseModel, ConfigDict

class PropertyModerationInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

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
    model_config = ConfigDict(extra="forbid")

    status: str
    review_comment: str
    property_id: str

class UserInfo(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    city: str
    role: str
    email: str
    whatsapp: int | str | None = None
    subscription: Optional[str] = None
    subscription_details: Optional[dict] = None
    subscription_expiry: Optional[str] = None

# ========== Property Detail Schemas ==========

class ResidentialSellDetails(BaseModel):
    model_config = ConfigDict(extra="forbid")

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
    model_config = ConfigDict(extra="forbid")

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
    model_config = ConfigDict(extra="forbid")

    monthly_rent: float
    negotiable: bool
    advance_amount: float
    utility_bills_included: bool
    address: str
    area_yards: float
    floor_number: Optional[str] = None
    description: Optional[str] = ""

class CommercialSellDetails(BaseModel):
    model_config = ConfigDict(extra="forbid")

    price: float
    negotiable: bool
    address: str
    area_yards: float
    floor_number: Optional[str] = None
    description: Optional[str] = ""

class AgriculturalLeaseDetails(BaseModel):
    model_config = ConfigDict(extra="forbid")

    rent_per_acre: float
    negotiable: bool
    address: str
    total_area: float
    lease_duration: int
    available_area: float
    description: Optional[str] = ""

class AgriculturalSellDetails(BaseModel):
    model_config = ConfigDict(extra="forbid")

    price_per_acre: float
    negotiable: bool
    address: str
    total_area: float
    available_area: float
    description: Optional[str] = ""

# ========== Main Property Model ==========

class PropertyInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    category: str  # "residential", "commercial", "agricultural"
    subcategory: str  # "rent", "sell", "lease"
    title: str
    images: List[str] = []

    residential_sell: Optional[ResidentialSellDetails] = None
    residential_rent: Optional[ResidentialRentDetails] = None
    commercial_rent: Optional[CommercialRentDetails] = None
    commercial_sell: Optional[CommercialSellDetails] = None
    agricultural_lease: Optional[AgriculturalLeaseDetails] = None
    agricultural_sell: Optional[AgriculturalSellDetails] = None

class RealEstateInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    is_real_estate_query: bool
    query: str

class Input(BaseModel):
    model_config = ConfigDict(extra="forbid")

    value: str
