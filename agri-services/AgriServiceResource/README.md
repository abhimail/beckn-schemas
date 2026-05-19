# AgriServiceResource Schema

**Container:** `Resource.resourceAttributes`
**Protocol Version:** 2.0
**Semantic Model:** generalised
**Use Cases:** Agri services discovery, livestock services, digital advisory, agri input services
**Tag:** service agri-services-ext resource

## Overview

AgriServiceResource extends the generalised Beckn `ServiceResource` schema with fields specific to agricultural and livestock services. It covers the full range of agricultural service types found in rural India and East Africa: veterinary visits, vaccination camps, brooding and incubation support, agricultural input supply, extension officer advisory, disease screening, and digital advisory services.

The schema is intentionally broad enough to serve both physical on-farm services (vaccination, screening) and information services (market price advisories, weather bulletins) under a single resource type. The `serviceCategory` and `providerType` enumerations distinguish between these modes at query and display time.

## Attachment Points

| Beckn Object | Field | Cardinality |
|---|---|---|
| `Resource` | `resourceAttributes` | 1..1 when schema active |

The schema is attached to `Resource.resourceAttributes`. A single catalog entry may expose one or more `Resource` objects each carrying one `resourceAttributes` block conforming to this schema.

## Design Rationale

Agricultural services require:

1. **Service categorisation** beyond generic service types — vaccination campaigns, brooding support, and input supply differ operationally from each other and from generic services.
2. **Provider typing** — the credentials and authorisations of a veterinarian, an extension officer, and a digital advisory platform differ materially and affect Seeker NP filtering.
3. **Livestock specificity** — a resource may be limited to poultry, or cattle, or mixed. Seeker NPs need to filter by the species they manage.
4. **Hierarchical geographic coverage** — rural East Africa and India use a village → ward → county/sub-district → country hierarchy that is more granular than the generic `coverageArea` in ServiceResource. The sub-schema `AgriServiceAreaHierarchy` models this explicitly, with an optional `coverageRadiusKm` for radius-based coverage.

These fields are entirely additive to `ServiceResource` — no inherited field is overridden or removed.

## Non-Goals

- This schema does not model the content of advisories (that is handled at the `performanceAttributes` level by `AgriDigitalPerformance`).
- It does not model financial terms (pricing, payment schedules) — those belong in `Offer.offerAttributes`.
- It does not model which specific animals were treated — that detail belongs in `performanceAttributes` (e.g. `AgriServicePerformance`).
- It does not replace or modify the base `ServiceResource` inherited fields (`serviceUnit`, `capacityPerDay`, `availabilitySchedule`, etc.).

## Upstream Candidates

The following fields are candidates for promotion to the base `ServiceResource` schema in a future generalised core release if sufficient adoption is observed across non-agri verticals:

| Field | Rationale for promotion |
|---|---|
| `coverageAreaCodes` | Coded administrative area references are useful for any location-bounded service |
| `serviceAreaHierarchy.coverageRadiusKm` | Radius-based coverage is domain-agnostic |
