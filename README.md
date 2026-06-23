 Race Telemetry Coach

## Project Goal
Race Telemetry Coach analyzes uploaded historical race telemetry and produces evidence-based driving insights. The project begins with validated CSV telemetry, then expands into analytics, containerization, Kubernetes, and an LLM-based coaching layer.

## Safety Boundary
This project analyzes historical telemetry only. It does not control a vehicle, provide real-time driving instructions, replace a qualified coach or engineer, or make safety-critical decisions.

## Supported Input
Lab 1 accepts one CSV contract:

Required columns:
- timestamp_s
- distance_m
- speed_kph
- lap_number

Optional channels:
- throttle_pct
- brake_pct
- steering_deg
- gear

## Data Handling
Do not commit private race telemetry, credentials, API keys, .pem files, or personal location data. Lab 1 uses small fictional CSV fixtures only.

## Cleanup Policy
Lab 1 creates no AWS infrastructure. Remove the Python virtual environment with `rm -rf .venv` only when the project is no longer needed. Later AWS labs will use the project teardown checklist and resource tracker created in Lab 0.
