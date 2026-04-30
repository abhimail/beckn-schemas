# HealthEntitlement — v2.1

**Schema Pack Version:** 2.1.0
**Released:** April 2026
**Network:** ONHS
**Status:** Initial release

## Notes

Health-domain extension of the generic-service ServiceEntitlement pattern.
Issued at UC0 procurement confirm. Consumed in UC1 (single-patient) and UC2
(camp multi-patient) engagements via `entitlementRef` in HealthConsideration.

### Container

- **Contract.contractAttributes**

### Relationship to ServiceEntitlement

HealthEntitlement carries the same core fields as ServiceEntitlement/v2.2 but adds:
- `healthServiceType` scoping the entitlement to a specific service category
- `campCommitment` sub-object for UC2 camp-allocation pattern

### Camp commitment pattern (UC2)

A camp commitment is a profile variant of HealthEntitlement — not a separate schema.
When `campCommitment` is present, the entitlement is allocated to a specific camp
date and location. `committedPatients` is set at UC0 commit; `confirmedPatients`
is populated at end-of-camp reconciliation and drives the on-actuals settlement
adjustment in HealthSettlement.

### Key features

- Health service type scoping (5 types)
- Full entitlement lifecycle: DRAFT → ACTIVE → LOW → EXPIRED → REVOKED → CLOSED
- Camp commitment sub-object with status tracking (SCHEDULED → ACTIVE → COMPLETED / CANCELLED)
- Geography and counterparty scoping
- Redemption rules (min/max per redemption, cooldown)
- Locked terms snapshot and grievance reference
