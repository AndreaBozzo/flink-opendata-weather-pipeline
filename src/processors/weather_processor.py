import json
from datetime import datetime, timezone
from typing import Optional, Dict, Any


class WeatherDataProcessor:
    """
    Classe di trasformazione per record meteo provenienti da
    sorgenti open (es. Open-Meteo API).
    Tutti i metodi sono statici per consentire l'uso diretto
    all'interno di operatori PyFlink (map, filter, ecc.).
    """

    # -------------------
    # VALIDATION
    # -------------------
    @staticmethod
    def validate(record: str) -> bool:
        """
        Valida che il record contenga la struttura base richiesta.
        Ritorna True se il campo 'current_weather' esiste e
        contiene dati essenziali.
        """
        try:
            data = json.loads(record)
            cw = data.get("current_weather", {})
            required = ["temperature", "windspeed", "time", "weathercode"]
            return all(k in cw for k in required)
        except (json.JSONDecodeError, TypeError):
            return False

    # -------------------
    # PROCESSING
    # -------------------
    @staticmethod
    def process(record: str) -> Optional[str]:
        """
        Aggiunge metadati di elaborazione (timestamp UTC).
        """
        try:
            data = json.loads(record)
            timestamp = datetime.now(timezone.utc).isoformat()
            data["processed_timestamp"] = timestamp
            return json.dumps(data)
        except (json.JSONDecodeError, TypeError):
            return None

    # -------------------
    # ENRICHMENT
    # -------------------
    @staticmethod
    def enrich(
        record: str, location: Optional[Dict[str, Any]] = None
    ) -> Optional[str]:
        """
        Aggiunge metadati geografici statici o dinamici al record.
        """
        try:
            data = json.loads(record)
            data["location"] = location or {
                "latitude": 45.4642,
                "longitude": 9.19,
                "city": "Milan",
                "country": "Italy",
            }
            return json.dumps(data)
        except (json.JSONDecodeError, TypeError):
            return None

    # -------------------
    # TRANSFORMATION
    # -------------------
    @staticmethod
    def transform(record: str) -> Optional[str]:
        """
        Estrae e normalizza i campi rilevanti per il downstream
        processing.
        """
        try:
            data = json.loads(record)
            cw = data["current_weather"]
            transformed_data = {
                "timestamp": cw["time"],
                "temperature": cw["temperature"],
                "windspeed": cw["windspeed"],
                "condition": cw["weathercode"],
                "processed_timestamp": data.get("processed_timestamp"),
                "is_heatwave": cw["temperature"] > 30,
                "location": data.get("location"),
            }
            return json.dumps(transformed_data)
        except (KeyError, json.JSONDecodeError, TypeError):
            return None
