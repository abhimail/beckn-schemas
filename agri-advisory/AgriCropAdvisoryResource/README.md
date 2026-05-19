# AgriCropAdvisoryResource Schema

**Container:** `Resource.resourceAttributes`
**Protocol Version:** 2.0
**Semantic Model:** generalised
**Use Cases:** UC1 — Crop Advisory (pest/disease alerts, sowing guidance, fertiliser schedules, irrigation advisories, harvest guidance)
**Tag:** agri-advisory resource crop

---

## Overview

`AgriCropAdvisoryResource` models a digital crop advisory capability that a Provider NP
(advisory platform) exposes for discovery and procurement by Seeker NPs (government agencies,
NGOs, implementing organisations).

A resource of this type describes *what kind* of advisory a platform can deliver — the crops
it covers, the crop growth stages it addresses, the advisory categories it produces, how often
it refreshes, and how far in advance it generates recommendations. The actual advisory content
is delivered out-of-band (app push, SMS, WhatsApp, IVR) once a contract is in place.

This schema extends `AgriServiceResource` (from the `agri-services-ext` pack), which in turn
extends `ServiceResource` from the `generic-service` pack. It inherits:

- `coverageAreaCodes` — machine-filterable geographic scope (LGD district/state codes for India)
- `languagesSupported` — BCP 47 language codes for farmer-facing content
- `serviceCategory` — always `DIGITAL_ADVISORY` for this resource type
- `providerType` — typically `DIGITAL_ADVISORY_PLATFORM`

---

## Attachment Points

| Field | Location in Beckn message |
|---|---|
| `resourceAttributes` | `catalog.resources[n].resourceAttributes` |
| Schema context | `context.schemaContext[]` entry referencing this schema's context.jsonld |

---

## Design Rationale

### Why `advisoryTypes` as an array?

A single advisory platform may deliver multiple advisory products under one contract (e.g.
pest alerts plus irrigation advisories for the same crop). Modelling this as an array allows
a Seeker NP to filter for providers that cover all required advisory types in a single resource,
reducing the number of separate contracts needed.

### Why `cropTypes` as CodedValue rather than free-text?

Machine-readable crop codes (AGROVOC or network-defined vocabulary) enable Seeker NPs to
programmatically match resources to scheme-specific crop lists without string parsing. The
`@context` field in each CodedValue identifies the vocabulary authority, making the code
unambiguous across networks.

### Why `advisoryLeadTimeDays`?

Sowing guidance and pre-season advisories must be delivered before the action window. A Seeker
NP configuring a government scheme procurement can filter for resources with sufficient lead
time to be actionable for the target farming population.

### Why `dataSourceRefs` as informational strings?

Transparency requirement: government procurers need to audit advisory quality. Formalising
data source references in the resource metadata makes this auditable without mandating a
machine-readable data source registry (which does not yet exist across Indian agri-data
providers).

---

## Non-Goals

- This schema does NOT model the advisory content itself (text, images, structured alert data).
  That is a delivery-layer concern resolved in the contract/fulfilment flow.
- This schema does NOT model farmer subscription preferences or notification channel settings.
  Those belong in `ServiceContract.bookingChannel`.
- This schema does NOT define crop classification codes. It references external authorities
  (AGROVOC, network-defined) via the CodedValue `@context` field.

---

## Upstream Candidates

The following properties are candidates for promotion to `AgriServiceResource` if other agri
resource schemas need them:

- `dataSourceRefs` — weather and commodity price resources also reference data sources;
  a common `dataSourceRefs` array at the `AgriServiceResource` level could reduce duplication.
- `advisoryUpdateFrequencyHours` — weather (`updateFrequencyHours`) and commodity price
  (`priceUpdateFrequencyHours`) have equivalent fields; a harmonised `contentUpdateFrequencyHours`
  at `AgriServiceResource` level is worth evaluating in the next schema review cycle.
