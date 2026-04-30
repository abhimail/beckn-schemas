# HealthEntitlement Schema

**Container:** `Contract.contractAttributes`
**Extends:** `ServiceEntitlement/v2.1`
**Protocol Version:** 2.0
**Semantic Model:** generalised
**Use Cases:** UC0 bulk procurement, UC2 camp engagement
**Tag:** health health-service contract

## Overview

HealthEntitlement captures the durable service-credit artifact issued when an implementing agency or payer organisation pre-purchases health service capacity from a Provider NP (UC0). It extends ServiceEntitlement with health service type scoping and a `campCommitment` sub-object for the UC2 camp-allocation pattern.

HealthEntitlement is created on the procurement Contract at confirm time and persists until its capacity is fully consumed, its validity period expires, or it is revoked. Consuming engagements (UC1 and UC2) reference it via `entitlementRef` in HealthConsideration to fund individual bookings without fresh payment authorisation.

## Attachment Points

Attaches to `Contract.contractAttributes` on the procurement Contract (UC0). The entitlement is the central artifact of the procurement model — it bridges the UC0 bulk commitment and the downstream UC1/UC2 consumption engagements.

## Design Rationale

- **`healthServiceType` scoping** — An entitlement is scoped to a specific health service type (e.g. DIAGNOSTIC_ANALYTICS). This prevents capacity purchased for cough analysis from being redeemed for teleconsultation, enforcing the commercial intent of the procurement contract. An implementing agency running multiple service programmes holds separate entitlements per service type.

- **`campCommitment` as an inline sub-object** — The UC2 camp pattern is a profile variant of the procurement model, not a separate use case. Rather than creating a separate CampEntitlement schema, the camp-specific fields (date, location, committedPatients, confirmedPatients, campStatus) are grouped in an optional `campCommitment` sub-object. When absent, the entitlement behaves as a standard rolling-consumption procurement. When present, it represents a fixed-date, fixed-location allocation.

- **`confirmedPatients` vs `committedPatients`** — The distinction is intentional and financially significant. `committedPatients` is set at camp booking (what was promised); `confirmedPatients` is populated at end-of-camp (what was delivered). The difference drives the `entitlementCreditBack` calculation in HealthSettlement. Keeping both fields explicit avoids any ambiguity in the reconciliation arithmetic.

- **Lifecycle alignment with ServiceEntitlement** — The full DRAFT → ACTIVE → LOW → EXPIRED → REVOKED → CLOSED state machine is inherited from ServiceEntitlement. The LOW state is particularly important in the health context: it signals to the implementing agency's programme management system that a top-up procurement should be initiated before field operations are disrupted.

## Non-Goals

- Does not model the per-patient or per-session contract — those are separate HealthContracts linked via `campId` / `entitlementRef`.
- Does not model the financial settlement of the procurement — that is HealthSettlement on the procurement Contract.
- Does not model clinical scope or service prerequisites — those belong in HealthResource.

## Upstream Candidates

- `campCommitment` sub-object (date, location, committed count, confirmed count, status) — the pattern of attaching a group-commitment profile to a bulk entitlement is applicable to any domain with event-based bulk service delivery (training camps, agricultural extension visits, community screening drives). Could be generalised in ServiceEntitlement as an optional `groupCommitment` sub-object.
- `healthServiceType` scoping — the pattern of scoping an entitlement to a specific service category (preventing cross-category redemption) is generic. Could be generalised in ServiceEntitlement as a `serviceCategory` scope field.
