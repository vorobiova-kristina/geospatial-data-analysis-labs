from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class TerritoryBase(BaseModel):
    name: str = Field(..., max_length=255)
    territory_type: str = Field(..., max_length=100)
    level: int = Field(..., ge=0)
    description: Optional[str] = Field(None, max_length=500)
    geom_wkt: str


class TerritoryCreate(TerritoryBase):
    pass


class TerritoryUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    territory_type: Optional[str] = Field(None, max_length=100)
    level: Optional[int] = Field(None, ge=0)
    description: Optional[str] = Field(None, max_length=500)
    geom_wkt: Optional[str] = None


class TerritoryRead(BaseModel):
    id: int
    name: str
    territory_type: str
    level: int
    description: Optional[str]
    geom_wkt: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class TerritoryMetricCreate(BaseModel):
    year: int
    population: Optional[int] = None
    area_km2: Optional[Decimal] = None
    source: Optional[str] = Field(None, max_length=255)


class TerritoryMetricUpdate(BaseModel):
    year: Optional[int] = None
    population: Optional[int] = None
    area_km2: Optional[Decimal] = None
    source: Optional[str] = Field(None, max_length=255)


class TerritoryMetricRead(BaseModel):
    id: int
    territory_id: int
    year: int
    population: Optional[int]
    area_km2: Optional[Decimal]
    source: Optional[str]
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
