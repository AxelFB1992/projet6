from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

# Liste des quartiers pour validation
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
    LargestPropertyUseType: Optional[str] = Field(None, description="Usage principal (ex: Office)")
    LargestPropertyUseTypeGFA: float = Field(0, ge=0)
    
    SecondLargestPropertyUseType: Optional[str] = Field(None, description="Second usage")
    SecondLargestPropertyUseTypeGFA: float = Field(0, ge=0)
    
    ThirdLargestPropertyUseType: Optional[str] = Field(None, description="Troisième usage")
    ThirdLargestPropertyUseTypeGFA: float = Field(0, ge=0)

    # Quartier
    Neighborhood: NeighborhoodName