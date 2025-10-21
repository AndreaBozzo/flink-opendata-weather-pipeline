"""Schemas for data validation and serialization.
Defines the structure of weather data used in the pipeline.
Uses Pydantic for data validation.
"""

from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class UnitSystem(str, Enum):
    metric = "metric"
    imperial = "imperial"


class WeatherData(BaseModel):
    temperature_c: float = Field(..., description="Temperature in Celsius")
    humidity: float = Field(..., ge=0, le=100, description="Humidity percentage")
    wind_speed_ms: float = Field(..., ge=0, description="Wind speed in m/s")
    latitude: float = Field(..., description="Latitude of the measurement")
    longitude: float = Field(..., description="Longitude of the measurement")
    city: str = Field(..., description="City name")
    country: str = Field(..., description="Country name")
    event_timestamp: datetime = Field(..., description="Time when the measurement occurred")
    source: str = Field(..., description="Data source identifier", example="open-meteo-api")
    unit_system: UnitSystem = Field(default=UnitSystem.metric, description="Unit system used")


class ProcessedWeatherData(WeatherData):
    temperature_f: float = Field(..., description="Temperature in Fahrenheit")
    wind_speed_kmh: float = Field(..., ge=0, description="Wind speed in km/h")
    is_heatwave: bool = Field(..., description="Indicates if temperature exceeds heatwave threshold")
    processed_timestamp: datetime = Field(default_factory=datetime.utcnow, description="Processing timestamp")
