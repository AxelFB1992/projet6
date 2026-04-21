from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

# --- Enum exhaustif pour les quariters ---
class NeighborhoodName(str, Enum):
    BALLARD = "BALLARD"
    CENTRAL = "CENTRAL"
    DELRIDGE = "DELRIDGE"
    DOWNTOWN = "DOWNTOWN"
    EAST = "EAST"
    GREATER_DUWAMISH = "GREATER DUWAMISH"
    LAKE_UNION = "LAKE UNION"
    MAGNOLIA_QUEEN_ANNE = "MAGNOLIA / QUEEN ANNE"
    NORTH = "NORTH"
    NORTHEAST = "NORTHEAST"
    NORTHWEST = "NORTHWEST"
    SOUTHEAST = "SOUTHEAST"
    SOUTHWEST = "SOUTHWEST"

# --- Enum exhaustif pour les Usages ---
class UsageType(str, Enum):
    # Bureau / Finance
    OFFICE = "Office"
    FINANCIAL_OFFICE = "Financial Office"
    BANK_BRANCH = "Bank Branch"
    
    # Logistique / Stockage
    NON_REFRIGERATED_WAREHOUSE = "Non-Refrigerated Warehouse"
    DISTRIBUTION_CENTER = "Distribution Center"
    PARKING = "Parking"
    SELF_STORAGE = "Self-Storage Facility"
    REFRIGERATED_WAREHOUSE = "Refrigerated Warehouse"
    
    # Commerce / Retail
    RETAIL_STORE = "Retail Store"
    STRIP_MALL = "Strip Mall"
    AUTO_DEALERSHIP = "Automobile Dealership"
    REPAIR_SERVICES = "Repair Services (Vehicle, Shoe, Locksmith, etc)"
    OTHER_MALL = "Other - Mall"
    OTHER_SERVICES = "Other - Services"
    LIFESTYLE_CENTER = "Lifestyle Center"
    PERSONAL_SERVICES = "Personal Services (Health/Beauty, Dry Cleaning, etc)"
    WHOLESALE_CLUB = "Wholesale Club/Supercenter"
    ENCLOSED_MALL = "Enclosed Mall"
    
    # Hôtellerie / Logement
    HOTEL = "Hotel"
    RESIDENCE_HALL = "Residence Hall/Dormitory"
    MULTIFAMILY = "Multifamily Housing"
    OTHER_LODGING = "Other - Lodging/Residential"
    
    # Éducation
    K12_SCHOOL = "K-12 School"
    UNIVERSITY = "College/University"
    OTHER_EDUCATION = "Other - Education"
    ADULT_EDUCATION = "Adult Education"
    PRE_SCHOOL = "Pre-school/Daycare"
    VOCATIONAL_SCHOOL = "Vocational School"
    
    # Culture / Loisirs / Culte
    WORSHIP = "Worship Facility"
    OTHER_RECREATION = "Other - Recreation"
    OTHER_ENTERTAINMENT = "Other - Entertainment/Public Assembly"
    SOCIAL_HALL = "Social/Meeting Hall"
    FITNESS = "Fitness Center/Health Club/Gym"
    MUSEUM = "Museum"
    PERFORMING_ARTS = "Performing Arts"
    MOVIE_THEATER = "Movie Theater"
    SWIMMING_POOL = "Swimming Pool"
    
    # Santé
    MEDICAL_OFFICE = "Medical Office"
    SENIOR_CARE = "Senior Care Community"
    HOSPITAL = "Hospital (General Medical & Surgical)"
    LABORATORY = "Laboratory"
    SPECIALTY_HOSPITAL = "Other/Specialty Hospital"
    URGENT_CARE = "Urgent Care/Clinic/Other Outpatient"
    RESIDENTIAL_CARE = "Residential Care Facility"
    
    # Commerce alimentaire
    SUPERMARKET = "Supermarket/Grocery Store"
    RESTAURANT = "Restaurant"
    OTHER_RESTAURANT_BAR = "Other - Restaurant/Bar"
    FOOD_SERVICE = "Food Service"
    BAR_NIGHTCLUB = "Bar/Nightclub"
    FOOD_SALES = "Food Sales"
    CONVENIENCE_STORE = "Convenience Store without Gas Station"
    FAST_FOOD = "Fast Food Restaurant"
    
    # Services publics / Industrie
    MANUFACTURING = "Manufacturing/Industrial Plant"
    DATA_CENTER = "Data Center"
    PRISON = "Prison/Incarceration"
    OTHER_PUBLIC = "Other - Public Services"
    OTHER_UTILITY = "Other - Utility"
    POLICE = "Police Station"
    COURTHOUSE = "Courthouse"
    FIRE_STATION = "Fire Station"
    OTHER_TECH = "Other - Technology/Science"
    LIBRARY = "Library"
    
    # Autre
    OTHER = "Other"

class BuildingInput(BaseModel):
    # Infos générales
    YearBuilt: int = Field(..., ge=1800, le=2026, description="Année de construction")
    NumberofBuildings: int = Field(1, ge=1)
    NumberofFloors: int = Field(..., ge=1)
    PropertyGFABuilding_s: float = Field(..., ge=0, alias="PropertyGFABuilding(s)")
    PropertyGFAParking: float = Field(0, ge=0)
    
    # Énergies
    Has_Steam: bool = False
    Has_Gas: bool = False
    Has_Electricity: bool = False  # Par défaut à False comme demandé

    # Usages et Surfaces (Top 3)
    LargestPropertyUseType: Optional[UsageType] = Field(None)
    LargestPropertyUseTypeGFA: float = Field(0, ge=0)
    
    SecondLargestPropertyUseType: Optional[UsageType] = Field(None)
    SecondLargestPropertyUseTypeGFA: float = Field(0, ge=0)
    
    ThirdLargestPropertyUseType: Optional[UsageType] = Field(None)
    ThirdLargestPropertyUseTypeGFA: float = Field(0, ge=0)

    # Quartier
    Neighborhood: NeighborhoodName