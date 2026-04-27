# SchemePerformance Schema

**Container:** `Performance.performanceAttributes`
**Protocol Version:** 2.0
**Semantic Model:** generalised
**Use Cases:** Agriculture scheme application lifecycle, agent-assisted enrollment, DBT benefit delivery, crop insurance claim tracking
**Tag:** agri-schemes scheme-discovery government-welfare performanceAttributes

---

## Overview

`SchemePerformance` models **how** a scheme benefit reaches the beneficiary — the delivery
mechanism, the application submission process, the assigned agent, and the domain-specific
lifecycle status codes for the application from booking through disbursement.

This is the execution layer. It does not describe what the scheme is (→ `SchemeResource`),
who is eligible (→ `SchemeOffer`), what benefit is committed (→ `SchemeConsideration`), or
how the disbursement is discharged (→ `SchemeSettlement`).

Migrated from: `SchemeFulfillmentAttributes` (v2, `fulfillmentAttributes` container). Prefix
changed from `sfa:` to `spe:`. The disbursementMode field has been moved to `SchemeSettlement`
where it describes the discharge channel.

---

## Attachment Points

| Container | Schema | Rationale |
|-----------|--------|-----------|
| `Performance.performanceAttributes` | `SchemePerformance` | Scheme delivery type, application submission mode, document collection mode, agent assignment, and application status codes are all execution-model properties. |

---

## Design Rationale

### 1. "Performance" is a better fit than "Fulfillment"
Government scheme benefit delivery is fundamentally a service or transfer execution — not
physical delivery. The v2.1 `Performance.mode` enum (DELIVERY / SERVICE / ACCESS / TRANSFER /
EXECUTION / OTHER) captures this cleanly. DBT schemes map to `mode: TRANSFER`; agent-assisted
applications map to `mode: SERVICE`. This was awkward in v2 where all schemes defaulted to
Fulfillment with type DELIVERY.

### 2. Domain status codes complement core Performance.status
The v2.1 core `Performance.status` (PLANNED / IN_PROGRESS / COMPLETED / FAILED / CANCELLED)
provides the coarse lifecycle. The domain-specific `spe:applicationStatus` adds 12 granular
states (BOOKING_CONFIRMED through BENEFIT_DISBURSED / CLAIM_SETTLED / BENEFIT_FAILED) that
are meaningful to BAPs tracking applicants through the government enrollment process.

### 3. disbursementMode moved to SchemeSettlement
In v2, `sfa:disbursementMode` (NEFT/RTGS/CHEQUE) lived in fulfillmentAttributes. In v2.1, it
describes how monetary settlement is discharged — correctly placed in `SchemeSettlement.settlementAttributes`. SchemePerformance retains only execution-model fields.

### 4. Agent-assisted fulfillment as first-class delivery type
The `spe:schemeDeliveryType = AGENT_ASSISTED_APPLICATION` value models the pattern where a
field agent submits the scheme application on the beneficiary's behalf. The `spe:agentDetails`
sub-schema captures the assigned agent's details.

---

## Non-Goals

- **No monetary transaction records.** Government application IDs and disbursement amounts belong in `SchemeContract` and `SchemeSettlement`.
- **No eligibility rules.** Who can apply is `SchemeOffer`.
- **No scheme content.** Scheme descriptions and required documents are `SchemeResource`.
- **No multi-stage logistics.** Scheme performance is modelled as a single-stage execution with rich status tracking.
- **No disbursement channel.** Disbursement mode (NEFT/RTGS) belongs in `SchemeSettlement`.

---

## Upstream Candidates

| Attribute | Rationale |
|-----------|-----------|
| `spe:applicationStatus` (generic) | A structured "service application lifecycle status" covering submitted → under-review → approved → rejected → disbursed is broadly applicable to any entitlement service vertical globally. |
| `spe:agentDetails` | A generic "assigned service agent" sub-schema applicable to any B2B2C service delivery vertical. |
| `spe:applicationPortalReference` | A generic "third-party portal reference ID" for cross-system application tracking. |
