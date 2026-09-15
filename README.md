# IntelliCharge V2 for Home Assistant

A modernized Home Assistant integration for IntelliCharge using the current IntelliCharge v2 API.

This integration provides access to IntelliCharge charging rules and allows direct management of battery settings from Home Assistant.

## Features

✅ Home Assistant Config Flow

✅ IntelliCharge cloud login

✅ Read custom charging rules

✅ Display charging rule information as sensors

✅ Support for Home Assistant Number entities

✅ Control minimum battery SOC after sell

✅ Uses the current IntelliCharge v2 API

## Installation

### HACS

1. Open HACS
2. Go to **Integrations**
3. Click **Custom repositories**
4. Add this repository URL
5. Select **Integration**
6. Install
7. Restart Home Assistant

### Manual Installation

Copy:

```text
custom_components/intellicharge
```

to:

```text
config/custom_components/intellicharge
```

Restart Home Assistant.

## Configuration

Go to:

```text
Settings
→ Devices & Services
→ Add Integration
→ IntelliCharge
```

Enter:

| Field | Value |
|---------|---------|
| Username | Your IntelliCharge username |
| Password | Your IntelliCharge password |
| Inverter ID | Your Plant ID |

Example:

```text
705
```

> Note:
>
> The current IntelliCharge API uses a Plant ID.
> Enter the Plant ID even though the field is named "Inverter ID".

## Entities

### Charging Rules Sensor

```text
sensor.intellicharge_charging_rules
```

Displays the number of active charging rules.

Attributes include:

```text
monday
tuesday
wednesday
thursday
friday
saturday
sunday

valid_from
valid_to

max_charge
max_discharge

max_battery_soc
min_battery_soc
min_battery_soc_for_sell
```

### Minimum Battery SOC After Sell

```text
number.intellicharge_min_soc_after_sell
```

Range:

```text
10% - 100%
```

This entity allows direct adjustment of:

```text
min_battery_soc_for_sell
```

within IntelliCharge.

## API Endpoints

The integration currently uses the IntelliCharge v2 API:

```text
POST /api/v1/login/access-token

GET  /api/v2/plants/{plant_id}

GET  /api/v2/plants/{plant_id}/settings/

GET  /api/v2/plants/{plant_id}/pvms-ems/custom-charging-rules/

POST /api/v2/plants/{plant_id}/pvms-ems/custom-charging-rules/
```

## Credits

This project is based on the original IntelliCharge Home Assistant integration created by:

https://github.com/ryjogo/hacs-intellicharge

The original project provided the foundation for IntelliCharge support in Home Assistant.

This fork has been updated and extended with:

- Support for the current IntelliCharge v2 API
- Plant-based configuration
- Improved authentication handling
- Updated Home Assistant compatibility
- Custom charging rule support
- Minimum Battery SOC After Sell control
- Native Home Assistant entities

Special thanks to **ryjogo** for creating the original integration.

## Disclaimer

This project is an unofficial Home Assistant integration and is not affiliated with, endorsed by, or maintained by IntelliCharge.

Use at your own risk.

## License

MIT License
