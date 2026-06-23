# Telemetry CSV Data Contract — Version 1

## Scope
Each CSV represents one lap or one continuous telemetry segment.

## Required Columns

| Column | Type | Rule |
|---|---|---|
| timestamp_s | decimal number | Must be 0 or greater and strictly increase row by row |
| distance_m | decimal number | Must be 0 or greater and never decrease within the file |
| speed_kph | decimal number | Must be between 0 and 500 |
| lap_number | whole number | Must be 1 or greater |

## Optional Columns

| Column | Type | Rule |
|---|---|---|
| throttle_pct | decimal number | 0 through 100 |
| brake_pct | decimal number | 0 through 100 |
| steering_deg | decimal number | -1080 through 1080 |
| gear | whole number | -1 through 12 |

## Handling Rules
- Missing required columns cause validation to fail.
- Missing optional columns generate a data-quality warning.
- Blank optional values are treated as unavailable data.
- Extra columns are accepted and ignored during Lab 1.
- A file with no data rows fails validation.
