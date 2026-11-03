from datetime import date

from pydantic import BaseModel, Field


class Meridlo(BaseModel):
    idi: str = Field(pattern=r"^KCZM\d{5}$")


class Kalibrace(BaseModel):
    id: str
    meridlo: Meridlo
    date: date
    campaign: str = Field(pattern=r"^\d{4}-\d{2}$")  # YYYY-MM
    inspection_location : str = "on site"
    inspection_note : str
    supplier: str = "KCZ"
    condition_temp: int
    condition_hum: int = Field(ge=0, le=100)
    v01: float  # TE
    v02: float  # TK
    v03: float = Field(ge=0, le=100)  # HE
    v04: float = Field(ge=0, le=100)  # HK
