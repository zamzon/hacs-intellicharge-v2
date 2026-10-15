# IntelliCharge V2 for Home Assistant

A modernized Home Assistant integration for IntelliCharge using the current IntelliCharge v2 API.

This integration provides access to IntelliCharge charging rules, current system status, and battery configuration directly from Home Assistant.

## Features

✅ Home Assistant Config Flow  
✅ IntelliCharge cloud login  
✅ Current IntelliCharge status sensor  
✅ Detailed status description sensor  
✅ Read custom charging rules  
✅ Control battery settings directly from Home Assistant  
✅ Support for Home Assistant Number entities  
✅ Support for IntelliCharge v2 API  
✅ Automatic updates every minute

---

## Installation

### HACS

1. Open HACS
2. Go to **Integrations**
3. Click **Custom Repositories**
4. Add:

```text
https://github.com/zamzon/hacs-intellicharge-v2
```

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

---

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
> IntelliCharge v2 uses a Plant ID.
> Enter the Plant ID even though the field is named "Inverter ID".

---

## Entities

### Status Sensors

#### sensor.intellicharge_current_action

Displays the current IntelliCharge action.

Examples:

```text
Eget forbrug
Opladning
Afladning
Standby
Låst
```

#### sensor.intellicharge_current_action_description

Displays the explanation shown in the IntelliCharge web application.

Examples:

```text
Systemet bruger den genererede energi til dit forbrug...
```

```text
Systemet oplader batteriet fra elnettet...
```

---

### Number Entities

#### number.intellicharge_min_soc_after_sell

Minimum battery SOC after sell.

Range:

```text
10% - 100%
```

#### number.intellicharge_min_battery_soc

Minimum battery SOC.

Range:

```text
10% - 100%
```

#### number.intellicharge_max_battery_soc

Maximum battery SOC.

Range:

```text
10% - 100%
```

#### number.intellicharge_max_charge

Maximum charging power.

Range:

```text
0 - 20000 W
```

#### number.intellicharge_max_discharge

Maximum discharge power.

Range:

```text
0 - 20000 W
```

---

### Advanced Sensor

#### sensor.intellicharge_charging_rules

Disabled by default.

Provides access to all active charging rules and attributes.

Available attributes include:

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

---

## Update Interval

The integration updates automatically every:

```text
1 minute
```

---

## API Endpoints

The integration currently uses:

```text
POST /api/v1/login/access-token

GET  /api/v2/plants/{plant_id}

GET  /api/v2/plants/{plant_id}/settings/

GET  /api/v2/plants/{plant_id}/pvms-ems/custom-charging-rules/

POST /api/v2/plants/{plant_id}/pvms-ems/custom-charging-rules/

GET  /api/v2/plants/{plant_id}/pvms-ems/actions/current
```

---

## Lovelace Example

```yaml
type: markdown
content: |
  ## IntelliCharge

  **{{ states('sensor.intellicharge_current_action') }}**

  {{ states('sensor.intellicharge_current_action_description') }}
```

---

## Credits

This project is based on:

https://github.com/ryjogo/hacs-intellicharge

Additional enhancements include:

- IntelliCharge v2 API support
- Plant-based configuration
- Current Action sensor
- Current Action Description sensor
- Battery SOC controls
- Charge and discharge power controls
- Improved Home Assistant compatibility
- Native Home Assistant entities

Special thanks to **ryjogo** for creating the original integration.

---

## Disclaimer

This is an unofficial Home Assistant integration and is not affiliated with, endorsed by, or maintained by IntelliCharge.

Use at your own risk.

---

## License

MIT License
