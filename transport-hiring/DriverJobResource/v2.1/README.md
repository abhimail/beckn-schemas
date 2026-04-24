# DriverJobResource v2.1

**Version:** 2.1.0  
**Extends:** `HiringJobResource` (via allOf)  
**Container:** `beckn:resourceAttributes`  
**Category:** `driver-job`

v2.1 release. Inherits all generic hiring fields from HiringJobResource and
adds driver-domain extensions: role_type, vehicle_categories_required,
shift_type, credential and training requirements, operator reputation capsule,
and stage-gated application_instructions.

## Delta Properties (v2.1 additions over base)

| Property | Type | Stage |
|---|---|---|
| `role_type` | DriverRoleType enum | on_discover |
| `vehicle_categories_required` | DriverVehicleCategory[] | on_discover |
| `shift_type` | ShiftType enum | on_discover |
| `working_hours` | string | on_discover |
| `contract_duration` | string (ISO 8601) | on_discover |
| `required_credentials` | CredentialType[] | on_discover |
| `required_training` | string[] | on_discover |
| `benefits_summary` | string[] | on_discover |
| `operator_reputation` | ReputationSummary | on_discover |
| `application_instructions` | string | **on_select only** |
