# agri-schemes — Beckn v2.1 Generalised Schema Pack

**Domain:** Agriculture and Government Welfare Scheme Discovery
**Protocol Version:** 2.0 (LTS)
**Semantic Model:** Generalised (Resource/Offer/Contract triad)
**Pack Version:** 2.1.0
**Status:** Under Review
**Migrated from:** agri-schemes v2 (Item/Offer/Order model)

---

## Overview

This schema pack enables Agriculture and Government Welfare Scheme Discovery on the Beckn
network. It models the full lifecycle of a welfare scheme — from discovery and eligibility
filtering through application, agent-assisted submission, benefit disbursement, and UC2
status enquiry for externally-enrolled beneficiaries.

The pack targets India's rural welfare schemes across central government (PM-JAY, PM-KISAN,
PMFBY, MGNREGS), state government, and NGO-funded programmes. Beneficiaries — primarily
farmers and rural households — can discover applicable schemes, check eligibility, apply
through the Beckn network, and track their application and disbursements.

---

## Schema Inventory

| Schema | Container | Prefix | IRI Base | Description |
|--------|-----------|--------|----------|-------------|
| `SchemeResource` | `resourceAttributes` | `sr:` | `https://schema.beckn.io/SchemeResource#` | Intrinsic scheme identity, type, funding model, required documents, benefit categories |
| `SchemeOffer` | `offerAttributes` | `sof:` | `https://schema.beckn.io/SchemeOffer#` | Eligibility criteria (demographic/economic/professional/identity/education/residency), benefit quantum, application window |
| `SchemePerformance` | `performanceAttributes` | `spe:` | `https://schema.beckn.io/SchemePerformance#` | Scheme delivery type, submission mode, document collection, agent assignment, application status lifecycle |
| `SchemeContract` | `contractAttributes` | `scr:` | `https://schema.beckn.io/SchemeContract#` | Government application reference, scheme outcome status, DPDP Act 2023 consent, UC2 external enrollment linkage |
| `SchemeConsideration` | `considerationAttributes` | `sco:` | `https://schema.beckn.io/SchemeConsideration#` | Committed benefit obligation (type, agreed amount, period) — new in v2.1 |
| `SchemeSettlement` | `settlementAttributes` | `sse:` | `https://schema.beckn.io/SchemeSettlement#` | Disbursement tranche record (PFMS reference, date, amount, installment number) — new in v2.1 |

---

## Use Cases

### UC1 — Scheme Discovery and Application (Beckn-native)
A farmer discovers welfare schemes through a Beckn BAP (e.g., KisaanApp), filters by
eligibility, and applies via an agent-assisted application process. The scheme authority
BPP tracks the application from booking through disbursement.

Key flows: `discover` → `select` → `init` → `confirm` → `status`

### UC2 — Status Enquiry for External Enrollment (Shadow Contract)
A farmer who enrolled in PM-KISAN or PMFBY through a non-Beckn channel (government portal,
CSC, bank branch) wants to check their application status via a Beckn BAP. The BAP creates
a "shadow tracking contract" using `scr:externalEnrollmentRef` + `scr:externalEnrollmentIdType`
to link the Beckn contract to the existing government enrollment.

Three-party contract: BENEFICIARY + SCHEME_AUTHORITY + PORTAL_OPERATOR.

---

## v2 → v2.1 Migration Summary

| v2 Schema | v2 Container | v2.1 Schema | v2.1 Container | Prefix change |
|-----------|-------------|-------------|----------------|---------------|
| SchemeItemAttributes | itemAttributes | SchemeResource | resourceAttributes | sia: → sr: |
| SchemeOfferAttributes | offerAttributes | SchemeOffer | offerAttributes | soa: → sof: |
| SchemeFulfillmentAttributes | fulfillmentAttributes | SchemePerformance | performanceAttributes | sfa: → spe: |
| SchemeOrderAttributes | orderAttributes | SchemeContract | contractAttributes | sor: → scr: |
| (new) | — | SchemeConsideration | considerationAttributes | — → sco: |
| (new) | — | SchemeSettlement | settlementAttributes | — → sse: |

Field redistributions:
- `sor:disbursementRecord` → dissolved into `SchemeConsideration` (amount) + `SchemeSettlement` (tranche detail)
- `sfa:disbursementMode` → moved to `SchemeSettlement.sse:disbursementMode`

---

## Key Design Wins in v2.1

**Multi-installment disbursement** — PM-KISAN's 3 × ₹2,000/year structure is now
first-class: one `SchemeConsideration` (₹6,000 total obligation) + three `SchemeSettlement`
objects (one per installment tranche with individual PFMS references).

**Three-party contracts** — Both UC1 (APPLICANT + SCHEME_AUTHORITY + FIELD_AGENT) and
UC2 (BENEFICIARY + SCHEME_AUTHORITY + PORTAL_OPERATOR) are expressed natively in
`Contract.participants[]`.

**Performance mode accuracy** — DBT schemes map to `mode: TRANSFER`, agent-assisted
application to `mode: SERVICE`. This is semantically cleaner than v2's Fulfillment with
implicit DELIVERY type.

**DPDP Act 2023 compliance fields** — `scr:applicantConsentGiven` + `scr:consentTimestamp`
are retained at contract level, correctly scoped to the whole application lifecycle.

---

## Upstream Candidates

| Attribute | Schema | Rationale |
|-----------|--------|-----------|
| `sof:eligibilityCriteria` (structured) | SchemeOffer | Six-dimension structured eligibility (demographic/economic/professional/identity/education/residency) is broadly applicable to any means-tested entitlement globally. |
| `sr:applicationModes` | SchemeResource | Generalised "access channel" concept applicable to any service or entitlement vertical. |
| `spe:agentDetails` | SchemePerformance | Generic "assigned service agent" sub-schema applicable to any B2B2C service delivery vertical. |
| `spe:applicationStatus` (generic form) | SchemePerformance | Structured service application lifecycle (submitted/under-review/approved/rejected/disbursed) applicable to permits, licences, grants globally. |

---

## Context Files

Each schema's `context.jsonld` is **fully self-contained** — no `@import` from external
core context URLs. Declare the relevant schema contexts in `Context.schemaContext` for
each Beckn message.

Example `schemaContext` for a full `on_confirm` payload:
```json
"schemaContext": [
  "https://schema.beckn.io/SchemeContract/v2.1/context.jsonld",
  "https://schema.beckn.io/SchemePerformance/v2.1/context.jsonld",
  "https://schema.beckn.io/SchemeConsideration/v2.1/context.jsonld",
  "https://schema.beckn.io/SchemeSettlement/v2.1/context.jsonld"
]
```
