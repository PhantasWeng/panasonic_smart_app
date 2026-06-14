# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) and other AI assistants when working with this repository.

## Project Overview

`panasonic_smart_app` is a **Home Assistant custom integration** that controls Panasonic air conditioners sold in **Taiwan**. Panasonic's Taiwan cloud API (`ems2.panasonic.com.tw`) is separate from Panasonic's global "Comfort Cloud" API, so the global integrations ([python-panasonic-comfort-cloud], [panasonic_ac]) do not work for Taiwanese units. This project wraps the Taiwan-specific cloud API and exposes air conditioners as Home Assistant `climate` entities.

- **Language:** Python (targets the Home Assistant runtime; not the maintainer's primary language)
- **Distribution:** [HACS](https://hacs.xyz/) custom repository + manual copy
- **IoT class:** Cloud Polling (`SCAN_INTERVAL = 300s`)
- **Device focus:** Air conditioners only (tested with PX/RX series using the `CZ-T007` Wi-Fi adapter)
- **Underlying protocol:** TaiSEIA 101 (Taiwan smart appliance standard)

> **Note on project status:** The README states this project is in maintenance mode. The maintainer recommends users migrate to the actively maintained fork at [osk2/panasonic_smart_app](https://github.com/osk2/panasonic_smart_app) for broader device support. Keep changes here conservative and focused on stability for air conditioners.

## Repository Structure

```
.
├── custom_components/
│   └── panasonic_smart_app/
│       ├── __init__.py          # Integration package docstring (no setup logic lives here)
│       ├── climate.py           # Home Assistant climate platform + PanasonicDevice entity
│       ├── manifest.json        # HA integration manifest (version, domain, codeowners)
│       └── smartApp/            # Standalone-ish API client package
│           ├── __init__.py      # SmartApp class: login, getDevices, getDeviceInfo, setCommand
│           ├── urls.py          # API endpoint URL builders (BASE_URL = ems2.panasonic.com.tw/api)
│           └── _taiseia.py      # TaiSEIA 101 command/option lookup tables
├── hacs.json                    # HACS metadata (domains: ["climate"])
├── manifest version             # (see custom_components/.../manifest.json)
├── CHANGELOG.md                 # Keep-a-Changelog format
├── README.md                    # User-facing docs (zh-TW + en)
├── info.md                      # HACS info panel content
├── LICENSE
└── .gitignore                   # ignores _test, __pycache__, secrets.py, *.pyc
```

## Architecture

The integration has two layers:

### 1. API client layer — `smartApp/`

`SmartApp` (in `smartApp/__init__.py`) is a thin synchronous client over the Panasonic Taiwan REST API using the `requests` library.

- **Auth:** `login()` POSTs `MemId`/`PW`/`AppToken` to `/userlogin1` and stores the returned `CPToken` in `self.header`. A hard-coded `APP_TOKEN` constant is required by the API.
- **Device discovery:** `getDevices()` GETs `/UserGetRegisteredGWList1`; the response (`GWList`) is cached on `self._devices`.
- **Read state:** `getDeviceInfo(deviceId, options=[...])` POSTs a list of `CommandType` hex codes to `/DeviceGetInfo` and flattens the response into a `{ "0xNN": status }` dict.
- **Write state:** `setCommand(deviceId, command, value)` GETs `/DeviceSetCommand` with the command/value as query params.
- Each request sets the per-device `auth` header and calls `response.raise_for_status()` — failures surface as exceptions.
- `urls.py` centralizes every endpoint as a function returning a URL string. Add new endpoints here, not inline.

### 2. Home Assistant platform layer — `climate.py`

- `setup_platform()` is the YAML platform entry point. It reads `username`/`password`, creates a `SmartApp`, logs in, and registers one `PanasonicDevice` per entry in `GWList`.
- `PanasonicDevice(ClimateEntity)` maps HA climate operations onto API calls. `update()` polls commands `0x00, 0x01, 0x03, 0x04, 0x21` (power, mode, target temp, current temp, outside temp).
- `@tryApiStatus` decorator wraps state-changing/polling methods: on **any** exception it re-runs `login()` once and retries the call. This is the token-refresh mechanism — preserve this behavior when editing those methods.

### 3. TaiSEIA mapping — `smartApp/_taiseia.py`

- `COMMANDS_NAME` maps hex `CommandType` codes to human names (some labels are in Traditional Chinese).
- `COMMANDS_OPTIONS` maps codes to enumerated values, most importantly `0x01` (mode) → Home Assistant `HVAC_MODE_*` constants.
- When supporting a new feature (fan speed, swing, nanoeX, etc.), extend these tables AND wire the corresponding command code into `climate.py`.

### Key command codes (TaiSEIA)

| Code   | Meaning            | Used in climate.py                |
|--------|--------------------|-----------------------------------|
| `0x00` | power (Off/On)     | `_is_on`, `set_hvac_mode` off/on  |
| `0x01` | mode (HVAC mode)   | `hvac_mode`, `set_hvac_mode`      |
| `0x02` | fan_speed          | not yet implemented               |
| `0x03` | target_temperature | `target_temperature`, `set_temperature` |
| `0x04` | current_temperature| `current_temperature`             |
| `0x21` | outside temperature| `outside_temperature`             |

## Development Workflow

There is **no build system, test suite, linter config, or CI** in this repo. It is a pure Home Assistant custom component loaded directly by the HA runtime.

### Testing changes

Changes must be validated inside a running Home Assistant instance:

1. Copy `custom_components/panasonic_smart_app/` into your HA config's `custom_components/` directory (or symlink it).
2. Add the platform config to `configuration.yaml`:
   ```yaml
   climate:
     - platform: panasonic_smart_app
       username: !secret smart_app_account
       password: !secret smart_app_password
   ```
3. Restart Home Assistant and watch the logs.
4. Enable debug logging to trace API calls and state updates:
   ```yaml
   logger:
     default: warning
     logs:
       custom_components.panasonic_smart_app: debug
   ```

Credentials are real Panasonic Taiwan smart-app accounts — never commit them. `secrets.py` is git-ignored for local experimentation.

### Versioning & releases

- Bump `version` in `custom_components/panasonic_smart_app/manifest.json` for each release.
- Record changes in `CHANGELOG.md` using the [Keep a Changelog](https://keepachangelog.com/) format already in use (sections: Added/Changed/Deprecated/Removed/Fixed/Security; an `[Unreleased]` section collects pending changes).
- Tags follow `vMAJOR.MINOR.PATCH` (e.g., `v0.1.1`) and feed the compare links at the bottom of `CHANGELOG.md`.
- `README.md` and `info.md` (HACS panel) overlap in content — keep configuration examples in sync when they change.

## Conventions

- **Dependencies:** Only the `requests` library (transitively available in HA) plus Home Assistant's own modules. `manifest.json` `requirements` is intentionally empty. Avoid adding new third-party dependencies.
- **API access:** Route every new endpoint through `smartApp/urls.py`; keep HTTP logic in `smartApp/__init__.py`, not in `climate.py`.
- **TaiSEIA codes:** Refer to commands by their hex code and add them to `_taiseia.py` tables rather than scattering magic strings.
- **Token resilience:** Use the `@tryApiStatus` decorator for any method that calls the API on the device, so an expired token transparently triggers re-login.
- **Logging:** Use the module `_LOGGER` (`logging.getLogger(__name__)`) at `debug` level for state/flow and `error` for user-facing failures (e.g., bad credentials). Do not log raw passwords (note the commented-out password log line in `climate.py` — keep it commented).
- **Naming:** Existing code mixes `camelCase` (API client methods like `getDevices`, `setCommand`) with Home Assistant's required `snake_case` entity methods (`set_hvac_mode`, `set_temperature`). Match the surrounding style of the file you edit.
- **Temperature range:** AC target temperature is clamped to 16–30 °C with a 1 °C step; unit is always Celsius.

## Important Caveats for AI Assistants

- This integration uses the **legacy YAML `setup_platform` API**, not config entries / config flow. Modernizing to config flow is a large change — only do it if explicitly requested.
- Several climate features (fan mode, swing mode, preset/eco, nanoeX) are **stubbed or commented out** in `climate.py`. The `SUPPORT_FLAGS` currently only enables `SUPPORT_TARGET_TEMPERATURE`. Don't assume stubs are functional.
- Home Assistant has deprecated many constants used here (e.g., `TEMP_CELSIUS`, `HVAC_MODE_*`, `SUPPORT_*` flags) in favor of newer enums (`UnitOfTemperature`, `HVACMode`, `ClimateEntityFeature`). The README acknowledges the code has not been migrated. If asked to fix compatibility with recent HA versions, this is the primary area to update — and it is a breaking, cross-cutting change.
- The API is undocumented and Taiwan-specific; behavior can only be confirmed against a real account and device.

[python-panasonic-comfort-cloud]: https://github.com/sockless-coding/panasonic_cc
[panasonic_ac]: https://github.com/DomiStyle/homeassistant-panasonic-ac
