from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from pydantic import BaseModel, ConfigDict, Field, field_validator


class Station(BaseModel):
    """Stacja pomiarowa (fizyczna lokalizacja z wieloma czujnikami)."""

    model_config = ConfigDict(populate_by_name=True)

    id: int = Field(alias="Identyfikator stacji")
    code: str = Field(alias="Kod stacji")
    name: str = Field(alias="Nazwa stacji")
    latitude: float = Field(alias="WGS84 φ N")
    longitude: float = Field(alias="WGS84 λ E")
    city_id: int = Field(alias="Identyfikator miasta")
    city_name: str = Field(alias="Nazwa miasta")
    commune: str = Field(alias="Gmina")
    district: str = Field(alias="Powiat")
    voivodeship: str = Field(alias="Województwo")
    street: str | None = Field(alias="Ulica", default=None)


class Sensor(BaseModel):
    """Stanowisko pomiarowe (pojedynczy czujnik w stacji)."""

    model_config = ConfigDict(populate_by_name=True)

    id: int = Field(alias="Identyfikator stanowiska")
    station_id: int = Field(alias="Identyfikator stacji")
    param_name: str = Field(alias="Wskaźnik")
    param_formula: str = Field(alias="Wskaźnik - wzór")
    param_code: str = Field(alias="Wskaźnik - kod")
    param_id: int = Field(alias="Id wskaźnika")


_ARCHIVAL_TZ = timezone(timedelta(hours=1))  # staly timezone dla danych archiwalnych


class ArchivalMeasurement(BaseModel):
    """Pojedynczy pomiar archiwalny z czujnika."""

    model_config = ConfigDict(populate_by_name=True)

    sensor_code: str = Field(alias="Kod stanowiska")
    timestamp: datetime = Field(alias="Data")
    value: float | None = Field(alias="Wartość")

    @field_validator("timestamp", mode="before")
    @classmethod
    def parse_timestamp(cls, v: str) -> datetime:
        naive = datetime.strptime(v, "%Y-%m-%d %H:%M:%S")
        return naive.replace(tzinfo=_ARCHIVAL_TZ)


class CurrentMeasurement(BaseModel):
    """Aktualny pomiar z czujnika"""

    model_config = ConfigDict(populate_by_name=True)

    sensor_code: str = Field(alias="Kod stanowiska")
    timestamp: datetime = Field(alias="Data")
    value: float | None = Field(alias="Wartość")

    @field_validator("timestamp", mode="before")
    @classmethod
    def parse_timestamp(cls, v: str) -> datetime:
        naive = datetime.strptime(v, "%Y-%m-%d %H:%M:%S")
        return naive.replace(tzinfo=ZoneInfo("Europe/Warsaw"))
