from pathlib import Path

import pytest

from app.telemetry_schema import TelemetryContractError, validate_telemetry_csv


SAMPLE_DATA = Path("sample_data")


def test_clean_lap_is_accepted():
    result = validate_telemetry_csv(SAMPLE_DATA / "clean_lap.csv")

    assert result.row_count == 4
    assert result.warnings == []


def test_missing_optional_channels_return_warning_not_failure():
    result = validate_telemetry_csv(SAMPLE_DATA / "missing_controls_lap.csv")

    assert result.row_count == 4
    assert "Optional channel not supplied: throttle_pct" in result.warnings
    assert "Optional channel not supplied: brake_pct" in result.warnings


def test_invalid_speed_is_rejected_with_field_name():
    with pytest.raises(TelemetryContractError) as error_info:
        validate_telemetry_csv(SAMPLE_DATA / "malformed_invalid_speed.csv")

    assert "speed_kph" in str(error_info.value)
