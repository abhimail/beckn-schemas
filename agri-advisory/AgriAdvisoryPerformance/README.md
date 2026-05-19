# AgriAdvisoryPerformance Schema

**Container:** `Performance.performanceAttributes`
**Protocol Version:** 2.0
**Semantic Model:** generalised
**Use Cases:** Advisory delivery confirmation, entitlement drawdown reconciliation, MIS reporting
**Tag:** agri-advisory performance

---

## Overview

`AgriAdvisoryPerformance` extends `AgriDigitalPerformance` (from `agri-services-ext`),
which itself extends `ServicePerformance` (from `generic-service`), to capture
advisory-specific delivery evidence on the Beckn Agri Advisory Network.

Each performance record documents a single advisory delivery event: the advisory
identifier, the advisory type, when the content was generated, the crop season it
applies to, how long it remains actionable, how many farmers were reached, which crops
it covers, and which data snapshot underpinned its generation.

These records are the primary evidence artefacts used for:
- **Entitlement drawdown reconciliation** — `farmersReached` units consumed against a
  pre-issued `ServiceEntitlement`.
- **Government MIS reporting** — advisory type, season, and farmer reach numbers feed
  into scheme monitoring dashboards.
- **Dispute resolution and audit** — `advisoryId`, `dataSnapshotRef`, and `generatedAt`
  support traceability back to the source data and content generation event.

---

## Attachment Points

`AgriAdvisoryPerformance` is attached at:

```
contract.performance[*].performanceAttributes
```

It appears in `on_status` and `on_update` responses from the Provider NP once an
advisory has been dispatched.

---

## Inheritance Chain

```
ServicePerformance  (generic-service)
└── AgriDigitalPerformance  (agri-services-ext)
    └── AgriAdvisoryPerformance  (agri-advisory-v21)  ← this schema
```

Fields inherited from `AgriDigitalPerformance`:
- `deliveryMode` — channel used (APP, SMS, WHATSAPP, IVR, etc.)
- `requestedLanguage` — BCP 47 language tag requested at confirm
- `deliveredLanguage` — BCP 47 language actually used for delivery
- `contentAccessUrl` — URL to access advisory content (if applicable)
- `contentAccessExpiry` — when the access URL expires
- `targetLocation` — CodedValue for the geographic scope of the advisory
- `contentRef` — Provider NP internal content reference
- `deliveredAt` — dispatch timestamp
- `deliveryConfirmed` — delivery receipt confirmed flag

Fields inherited from `ServicePerformance`:
- `providerConfirmedCompletion` / `clientConfirmedCompletion`
- `serviceNotes`, `followUpRequired`, `followUpDate`

---

## Design Rationale

### Why `farmersReached` and not a unit counter at the contract level?
In bulk procurement flows a single on_status call may cover delivery to thousands of
farmers simultaneously. `farmersReached` at the performance record level provides the
unit count needed for entitlement drawdown without requiring per-farmer individual
records.

### `advisoryId` vs Beckn `Performance.id`
`Performance.id` is the Beckn network-level identifier for the performance event.
`advisoryId` is the Provider NP's internal advisory instance identifier — used for
re-fetch, duplicate detection, and grievance linkage at the application layer. Both
are preserved for maximum traceability.

### `cropTypes` as CodedValue array
Crop identification requires both a code (from a recognised authority such as FAO
AGROVOC or ICAR) and a display name. `CodedValue` (from `agri-common`) provides this
structure and is consistent with crop identification in the resource schemas.

### `dataSnapshotRef`
Regulatory and audit requirements in government advisory schemes increasingly require
evidence of the data that underpinned an advisory recommendation. `dataSnapshotRef`
provides a lightweight pointer to the Provider NP's internal snapshot record without
requiring the full data to be embedded in the performance payload.

---

## Non-Goals

- **Delivery channel setup or configuration** — governed by `AgriAdvisoryOffer.deliveryChannels`.
- **Content quality assessment or farmer feedback** — not in scope; may be handled via
  separate rating/review mechanisms.
- **Financial settlement calculation** — handled by `ServiceSettlement`; `farmersReached`
  feeds the input to settlement but does not drive it directly.

---

## Upstream Candidates

The following fields may be proposed for upstream inclusion in future versions of
`AgriDigitalPerformance` in `agri-services-ext` if they prove reusable across
advisory domains:

- `validityWindowHours` — applicable to any time-sensitive digital advisory (weather,
  health, financial) delivered via Beckn.
- `farmersReached` / equivalent beneficiary count — applicable to any bulk public
  service delivery performance record.
