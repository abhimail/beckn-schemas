# ONHS Health* Schema Pack

**Network:** Open Network for Health Services (ONHS)
**Protocol Version:** Beckn 2.0
**Schema Version:** 2.1.0
**Semantic Model:** generalised
**Status:** Initial release

## Overview

The ONHS Health* schema pack provides domain extension schemas for health services on the Open Network for Health Services. Each schema extends the corresponding [generic-service](../../generic-service/) base schema and adds health-specific attributes. The pack covers the full transaction lifecycle from service discovery through procurement, patient engagement, clinical delivery, and settlement.

The schemas were designed from an analysis of three representative use cases but are intended to be applicable across health service contexts more broadly.

## Schemas

This pack includes 8 extension schemas:

1. **HealthResource** — Health service resource attributes (service type, clinical validation, service prerequisites, analytics engine specs)
2. **HealthOffer** — Health offer terms (offer type, health service scoping, bulk procurement constraints)
3. **HealthContract** — Contract metadata carrying the `healthServiceType` discriminator that drives conditional field requirements across sibling schemas
4. **HealthPerformance** — Clinical execution details (appointment, location, clinical interpretation, artefacts generated, data deletion attestation)
5. **HealthConsideration** — Health-specific pricing and payment terms (inherits full ServiceConsideration, adds per-patient billing and camp cash collection)
6. **HealthSettlement** — Settlement with entitlement traceability, credit-back mechanics, and camp ledger linkage
7. **HealthEntitlement** — Pre-purchased health service capacity with health service type scoping and camp commitment sub-object
8. **HealthParticipant** — Health network participant roles (patient identity, specialist credentials, payer details, field worker linkage)

## Base Pack Dependency

All Health* schemas extend the `generic-service` base pack. The base pack must be present for cross-schema `$ref` resolution. Base schemas extended:

| Health Schema | Extends |
|---|---|
| HealthResource | ServiceResource |
| HealthOffer | ServiceOffer |
| HealthContract | ServiceContract |
| HealthPerformance | ServicePerformance |
| HealthConsideration | ServiceConsideration |
| HealthSettlement | ServiceSettlement |
| HealthEntitlement | ServiceEntitlement |
| HealthParticipant | *(standalone — no base)* |

## Use Cases

- **UC0 — Bulk Procurement**: Implementing agency pre-purchases health service capacity from a provider. Issues a HealthEntitlement at confirm.
- **UC1 — Single Patient Engagement**: Patient or field worker books a health service for one patient. Funded by fresh payment or entitlement drawdown.
- **UC2 — Camp Engagement**: Implementing agency commits to a multi-patient screening camp. Uses HealthEntitlement with `campCommitment` sub-object; settles on-actuals at end of camp.

## Transaction Flow

### Standard (pay-per-engagement) — UC1
1. **Discovery** (on_discover): HealthResource + HealthOffer in catalog
2. **Confirmation** (on_confirm): HealthContract, HealthPerformance, HealthConsideration (paymentAuthorisation)
3. **Status** (on_status): HealthPerformance updates, HealthSettlement

### Procurement + drawdown — UC0 → UC1
1. **Procurement** (on_confirm): HealthContract, HealthConsideration (milestone), HealthEntitlement issued
2. **Consuming engagement** (on_confirm per patient): HealthContract, HealthPerformance, HealthConsideration (entitlementRef)
3. **Reconciliation** (on_status / update): HealthSettlement with on-actuals adjustment; entitlement capacity updated

### Camp — UC2
1. **Camp commitment** (on_confirm): HealthEntitlement with campCommitment (date, location, committedPatients)
2. **Camp execution** (on_status updates): HealthPerformance per patient
3. **End-of-camp reconciliation** (update): HealthSettlement — adjustmentType ON_ACTUALS, entitlementCreditBack for undelivered units

## healthServiceType Discriminator

The `healthServiceType` field in HealthContract is the central discriminator for the pack. Its value makes certain fields conditionally required in sibling schemas:

| Value | Description |
|---|---|
| DIAGNOSTIC_ANALYTICS | AI-driven analysis of patient samples (e.g. cough analysis, cancer screening) |
| TELECONSULTATION | Remote consultation with a licensed practitioner |
| PHYSICAL_CONSULTATION | In-person consultation (direct or referred) |
| RADIOLOGY | Imaging and radiology report interpretation |
| LAB_TEST | Pathology or laboratory diagnostic test |

## Namespace Prefixes

- `hr:` — HealthResource
- `hof:` — HealthOffer
- `hct:` — HealthContract
- `hpm:` — HealthPerformance
- `hcn:` — HealthConsideration
- `hsl:` — HealthSettlement
- `hen:` — HealthEntitlement
- `hpt:` — HealthParticipant
