# HealthOffer Schema

**Container:** `Offer.offerAttributes`
**Extends:** `ServiceOffer/v2.1`
**Protocol Version:** 2.0
**Semantic Model:** generalised
**Use Cases:** UC0 bulk procurement, UC1 single patient engagement, UC2 camp engagement
**Tag:** health health-service offer

## Overview

HealthOffer captures health-specific commercial and operational terms for a service offering on the ONHS network. It extends ServiceOffer with a health service type scope, an offer type discriminator (SINGLE_EVENT / BULK_PROCUREMENT / CAMP), and conditional mandatory fields for bulk procurement offers.

An Offer is the commercial wrapper around a Resource — it says *under what terms the Resource may be booked*, not what the Resource is. One Resource can have multiple Offers (e.g. a single-session offer and a bulk procurement offer for the same cough analysis service).

## Attachment Points

Attaches to `Offer.offerAttributes`. Published alongside HealthResource in `on_discover` catalog responses. Each Offer references one or more Resources via `resourceIds` and one or more Considerations via `considerationIds`.

## Design Rationale

- **`offerType` as the primary commercial discriminator** — SINGLE_EVENT covers UC1 individual bookings, BULK_PROCUREMENT covers UC0 institutional pre-purchase, and CAMP covers UC2 multi-patient camp commitments. The offer type determines which transaction flow applies and drives conditional mandatory field rules: BULK_PROCUREMENT requires `minimumQuantity`, `maximumQuantity`, and `validityPeriodDays`; CAMP requires `campMaxPatients` and `campDurationHours`.

- **`healthServiceType` scoping on Offer** — An Offer may restrict itself to a specific health service type, enabling a provider to publish different commercial terms for TELECONSULTATION vs DIAGNOSTIC_ANALYTICS on the same resource. A null/absent `healthServiceType` on the Offer means it applies to any service type the resource supports.

- **Cancellation policies inherited from ServiceOffer** — The structured cancellation policy array (hours-before-service → refund fraction) is defined in the ServiceOffer base and applies unchanged. Health-specific cancellation behaviour (e.g. no-show policy for teleconsultation) is expressed through the same structure with appropriate `hoursBeforeService: 0` entries.

## Non-Goals

- Does not model the per-patient unit price or payment methods — those belong in HealthConsideration.
- Does not model the entitlement capacity or drawdown rules — those belong in HealthEntitlement.
- Does not model the clinical scope or service prerequisites of the resource — those belong in HealthResource.

## Upstream Candidates

- `offerType` enum (SINGLE_EVENT / BULK_PROCUREMENT / CAMP) — the pattern of discriminating commercial model via an offer type is applicable across service domains (e.g. single booking vs. subscription vs. group booking). Could be generalised in the ServiceOffer base as an `engagementModel` field.
