import json
from datetime import timedelta
from pathlib import Path

from smog.ingestion.models import ArchivalMeasurement, CurrentMeasurement, Sensor, Station


def test_station_parses_real_response() -> None:
    raw = json.loads(Path("tests/fixtures/gios_stations_sample.json").read_text(encoding="utf-8"))
    stations = raw["Lista stacji pomiarowych"]

    warsaw = next(s for s in stations if s["Nazwa stacji"] == "Warszawa, Al. Niepodległości")
    station = Station.model_validate(warsaw)

    assert station.id == 530
    assert station.name == "Warszawa, Al. Niepodległości"
    assert isinstance(station.latitude, float)


def test_archival_measurement_parses_timezone() -> None:
    raw = {
        "Kod stanowiska": "MzWarAlNiepo-PM2.5-1g",
        "Data": "2025-01-01 01:00:00",
        "Wartość": 65.7,
    }

    m = ArchivalMeasurement.model_validate(raw)

    assert m.value == 65.7
    assert m.timestamp.utcoffset() == timedelta(hours=1)
    assert m.timestamp.tzinfo is not None


def test_sensor_parses_real_response() -> None:
    raw = json.loads(Path("tests/fixtures/gios_sensors_sample.json").read_text(encoding="utf-8"))
    sensors = raw["Lista stanowisk pomiarowych dla podanej stacji"]

    warsaw_pm25 = next(
        s
        for s in sensors
        if s["Wskaźnik - kod"] == "PM2.5" and s["Identyfikator stacji"] == 530  # noqa: E501
    )
    sensor = Sensor.model_validate(warsaw_pm25)

    assert sensor.param_code == "PM2.5"
    assert sensor.station_id == 530
    assert sensor.id == 3585


def test_current_measurement_parses_summer_timezone() -> None:
    raw = {
        "Kod stanowiska": "MzWarAlNiepo-PM2.5-1g",
        "Data": "2025-07-01 01:00:00",
        "Wartość": 65.7,
    }

    m = CurrentMeasurement.model_validate(raw)

    assert m.value == 65.7
    assert m.timestamp.utcoffset() == timedelta(hours=2)
    assert m.timestamp.tzinfo is not None


def test_current_measurement_parses_winter_timezone() -> None:
    raw = {
        "Kod stanowiska": "MzWarAlNiepo-PM2.5-1g",
        "Data": "2025-01-01 01:00:00",
        "Wartość": 65.7,
    }

    m = CurrentMeasurement.model_validate(raw)

    assert m.value == 65.7
    assert m.timestamp.utcoffset() == timedelta(hours=1)
    assert m.timestamp.tzinfo is not None
