from __future__ import annotations

import sys
from pathlib import Path

from app.telemetry_schema import TelemetryContractError, validate_telemetry_csv


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python -m app.validate_csv <path-to-csv>")
        return 2

    csv_path = Path(sys.argv[1])

    try:
        result = validate_telemetry_csv(csv_path)
    except TelemetryContractError as error:
        print(f"INVALID TELEMETRY FILE:\n{error}")
        return 1

    print(f"VALID TELEMETRY FILE: {csv_path}")
    print(f"Rows accepted: {result.row_count}")

    if result.warnings:
        print("DATA-QUALITY WARNINGS:")
        for warning in result.warnings:
            print(f"- {warning}")
    else:
        print("DATA-QUALITY WARNINGS: none")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
