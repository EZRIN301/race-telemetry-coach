from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator


REQUIRED_COLUMNS = {
    "timestamp_s",
    "distance_m",
    "speed_kph",
    "lap_number",
}

OPTIONAL_COLUMNS = {
    "throttle_pct",
    "brake_pct",
    "steering_deg",
    "gear",
}


class TelemetryContractError(ValueError):
    """Raised when a telemetry CSV does not meet the project data contract."""


class TelemetryRow(BaseModel):
    """One validated telemetry record."""

    model_config = ConfigDict(extra="ignore")

    timestamp_s: float = Field(ge=0)
    distance_m: float = Field(ge=0)
    speed_kph: float = Field(ge=0, le=500)
    lap_number: int = Field(ge=1)

    throttle_pct: float | None = Field(default=None, ge=0, le=100)
    brake_pct: float | None = Field(default=None, ge=0, le=100)
    steering_deg: float | None = Field(default=None, ge=-1080, le=1080)
    gear: int | None = Field(default=None, ge=-1, le=12)

    @field_validator(
        "throttle_pct",
        "brake_pct",
        "steering_deg",
        "gear",
        mode="before",
    )
    @classmethod
    def blank_optional_values_are_none(cls, value):
        """Treat blank optional CSV values as unavailable telemetry."""
        if value is None:
            return None
        if isinstance(value, str) and not value.strip():
            return None
        return value


@dataclass(frozen=True)
class ValidationResult:
    rows: list[TelemetryRow]
    warnings: list[str]

    @property
    def row_count(self) -> int:
        return len(self.rows)


def validate_telemetry_csv(csv_path: str | Path) -> ValidationResult:
    """Validate a telemetry CSV against the Lab 1 contract."""

    path = Path(csv_path)

    if not path.exists():
        raise TelemetryContractError(f"Telemetry file not found: {path}")

    with path.open("r", encoding="utf-8", newline="") as file_handle:
        reader = csv.DictReader(file_handle)

        if not reader.fieldnames:
            raise TelemetryContractError("CSV header row is missing.")

        headers = [header.strip() for header in reader.fieldnames if header]
        reader.fieldnames = headers

        if len(headers) != len(set(headers)):
            raise TelemetryContractError("CSV contains duplicate column names.")

        missing_required = sorted(REQUIRED_COLUMNS - set(headers))
        if missing_required:
            raise TelemetryContractError(
                "Missing required column(s): " + ", ".join(missing_required)
            )

        warnings = [
            f"Optional channel not supplied: {column}"
            for column in sorted(OPTIONAL_COLUMNS - set(headers))
        ]

        validated_rows: list[TelemetryRow] = []
        previous_timestamp: float | None = None
        previous_distance: float | None = None

        for row_number, raw_row in enumerate(reader, start=2):
            cleaned_row = {
                key: value.strip() if isinstance(value, str) else value
                for key, value in raw_row.items()
                if key is not None
            }

            try:
                row = TelemetryRow.model_validate(cleaned_row)
            except ValidationError as error:
                raise TelemetryContractError(
                    f"Row {row_number} failed validation:\n{error}"
                ) from error

            if previous_timestamp is not None and row.timestamp_s <= previous_timestamp:
                raise TelemetryContractError(
                    f"Row {row_number}: timestamp_s must be strictly increasing. "
                    f"Previous={previous_timestamp}, current={row.timestamp_s}."
                )

            if previous_distance is not None and row.distance_m < previous_distance:
                raise TelemetryContractError(
                    f"Row {row_number}: distance_m must not decrease. "
                    f"Previous={previous_distance}, current={row.distance_m}."
                )

            validated_rows.append(row)
            previous_timestamp = row.timestamp_s
            previous_distance = row.distance_m

    if not validated_rows:
        raise TelemetryContractError("CSV contains no telemetry data rows.")

    return ValidationResult(rows=validated_rows, warnings=warnings)
