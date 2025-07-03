# // ==========================
# // RESIDENTIAL SELL
# // ==========================

# /* ✅ FRONTEND Payload Example */
# {
#   category: "residential",
#   subcategory: "sell",
#   title: "3 Marla House",
#   images: [],
#   residential_sell: {
#     price: 3500000,
#     negotiable: true,
#     address: "Street 1, Lahore",
#     bedrooms: 3,
#     bathrooms: 2,
#     story: "Double",
#     total_area_yards: 60,
#     documents: "documented",
#     description: "Corner house with good ventilation"
#   }
# }

# /* 🧾 BACKEND Expected Input */
# class ResidentialSellDetails(BaseModel):
#     price: float
#     negotiable: bool
#     address: str
#     bedrooms: int
#     bathrooms: int
#     story: str
#     total_area_yards: float
#     documents: str  # "documented" | "kacha"
#     description: Optional[str] = ""



# // ==========================
# // RESIDENTIAL RENT
# // ==========================

# /* ✅ FRONTEND Payload Example */
# {
#   category: "residential",
#   subcategory: "rent",
#   title: "Upper Portion for Rent",
#   images: [],
#   residential_rent: {
#     monthly_rent: 25000,
#     negotiable: false,
#     advance_amount: 50000,
#     utility_bills_included: true,
#     address: "DHA Phase 2, Karachi",
#     bedrooms: 2,
#     bathrooms: 2,
#     story: "Upper",
#     floor_number: "1st",
#     total_area_yards: 80,
#     description: "Ideal for small family"
#   }
# }

# /* 🧾 BACKEND Expected Input */
# class ResidentialRentDetails(BaseModel):
#     monthly_rent: float
#     negotiable: bool
#     advance_amount: float
#     utility_bills_included: bool
#     address: str
#     bedrooms: int
#     bathrooms: int
#     story: str
#     floor_number: Optional[str] = None
#     total_area_yards: Optional[float] = None
#     description: Optional[str] = ""


# // ==========================
# // COMMERCIAL SELL
# // ==========================

# /* ✅ FRONTEND Payload Example */
# {
#   category: "commercial",
#   subcategory: "sell",
#   title: "Shop in Saddar",
#   images: [],
#   commercial_sell: {
#     price: 9000000,
#     negotiable: true,
#     address: "Main Saddar Bazar",
#     area_yards: 120,
#     floor_number: "Ground",
#     description: "Main road-facing shop"
#   }
# }

# /* 🧾 BACKEND Expected Input */
# class CommercialSellDetails(BaseModel):
#     price: float
#     negotiable: bool
#     address: str
#     area_yards: float
#     floor_number: Optional[str] = None
#     description: Optional[str] = ""


# // ==========================
# // COMMERCIAL RENT
# // ==========================

# /* ✅ FRONTEND Payload Example */
# {
#   category: "commercial",
#   subcategory: "rent",
#   title: "Office Space",
#   images: [],
#   commercial_rent: {
#     monthly_rent: 60000,
#     negotiable: true,
#     advance_amount: 180000,
#     utility_bills_included: false,
#     address: "Blue Area, Islamabad",
#     area_yards: 200,
#     floor_number: "3rd",
#     description: "Furnished office with AC"
#   }
# }

# /* 🧾 BACKEND Expected Input */
# class CommercialRentDetails(BaseModel):
#     monthly_rent: float
#     negotiable: bool
#     advance_amount: float
#     utility_bills_included: bool
#     address: str
#     area_yards: float
#     floor_number: Optional[str] = None
#     description: Optional[str] = ""


# // ==========================
# // AGRICULTURAL SELL
# // ==========================

# /* ✅ FRONTEND Payload Example */
# {
#   category: "agricultural",
#   subcategory: "sell",
#   title: "Farm Land for Sale",
#   images: [],
#   agricultural_sell: {
#     price_per_acre: 1500000,
#     negotiable: true,
#     address: "Gujranwala outskirts",
#     total_area: 12,
#     available_area: 10,
#     description: "Tube well and canal available"
#   }
# }

# /* 🧾 BACKEND Expected Input */
# class AgriculturalSellDetails(BaseModel):
#     price_per_acre: float
#     negotiable: bool
#     address: str
#     total_area: float
#     available_area: float
#     description: Optional[str] = ""


# // ==========================
# // AGRICULTURAL LEASE (or rent)
# // ==========================

# /* ✅ FRONTEND Payload Example */
# {
#   category: "agricultural",
#   subcategory: "lease", // or "rent"
#   title: "Lease Land 5 Acres",
#   images: [],
#   agricultural_lease: {
#     rent_per_acre: 50000,
#     negotiable: false,
#     lease_duration: 3,
#     address: "Multan Road",
#     total_area: 5,
#     available_area: 5,
#     description: "Best for seasonal crops"
#   }
# }

# /* 🧾 BACKEND Expected Input */
# class AgriculturalLeaseDetails(BaseModel):
#     rent_per_acre: float
#     negotiable: bool
#     address: str
#     total_area: float
#     available_area: float
#     description: Optional[str] = ""
# property-> residential -> rent
# property -> commercial -> rent
# agricultural -> rent invalid form selection