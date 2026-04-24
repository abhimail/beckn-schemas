# DriverCandidateProfileResource v2.1

**Version:** 2.1.0  
**Extends:** `CandidateProfileResource` (via allOf)  
**Container:** `beckn:resourceAttributes`  
**Category:** `driver-candidate`

v2.1 release. Extends CandidateProfileResource with driver-domain fields.

## Delta Properties

| Property | Type | PII | Stage |
|---|---|---|---|
| `driver_role_types` | DriverRoleType[] | No | on_discover |
| `vehicle_categories` | DriverVehicleCategory[] | No | on_discover |
| `home_location` | NetworkLocation | Partial (locality only) | on_discover |
| `reputation_summary` | ReputationSummary | No | on_discover |
| `credential_summary` | CredentialType[] | No | on_discover |
| `training_summary` | string[] | No | on_discover |
| `passport_reference` | string | **Yes** | **init+** |
| `last_updated` | date-time | No | on_discover |
