# AgriAdvisoryOffer Schema

**Container:** `Offer.offerAttributes`
**Protocol Version:** 2.0
**Semantic Model:** generalised
**Use Cases:** Bulk procurement of advisory capacity, individual farmer subscriptions
**Tag:** agri-advisory offer

---

## Overview

`AgriAdvisoryOffer` extends `ServiceOffer` (from `generic-service`) to describe the
offer terms for packaged agricultural advisory services on the Beckn Agri Advisory
Network. It captures which resource types are bundled in the offer, which languages
are available, the subscription duration and volume, the target beneficiary class,
and the delivery channels through which advisories will reach farmers.

The schema is intentionally lean: it delegates pricing, quantity, validity, bulk
discount, and cancellation policy to the inherited `ServiceOffer` fields and adds
only the domain-specific dimensions that differ across advisory offers.

---

## Attachment Points

`AgriAdvisoryOffer` is attached at:

```
catalogs[*].offers[*].offerAttributes
```

It may also appear inside a nested offer bundle, where a single offer packages
multiple resource types (e.g. crop advisory + weather forecast + commodity price).

---

## Design Rationale

### Why not extend `AgriServiceOffer`?
`AgriServiceOffer` (from `agri-services-ext`) adds `inputBrandOrVariety` — a field
relevant for physical input supply services (seeds, fertilisers) but irrelevant for
digital advisory. Extending directly from `ServiceOffer` keeps the schema clean.

### `entitlementEligible` flag
Government schemes and NGO programmes typically pre-purchase advisory capacity via a
`ServiceEntitlement`. The `entitlementEligible` flag signals to Seeker NPs (and their
search/filter logic) that this offer can be funded via entitlement drawdown at confirm
time using `ServiceConsideration.entitlementRef`.

### `bundledResourceTypes`
Allows a single offer to bundle multiple advisory resource types. This is common in
premium agri advisory offers where a crop advisory subscription also includes weather
forecasts and commodity price alerts. The values correspond to `x-tags` of the
included resource schemas (`AgriCropAdvisoryResource`, `AgriWeatherResource`,
`AgriCommodityPriceResource`).

### `deliveryChannels`
Advisory delivery channels must be agreed at the offer level so that Seeker NPs can
match offers to their last-mile infrastructure (e.g. an NGO with a WhatsApp-based
farmer network vs. a government scheme using IVR). At fulfilment, the specific channel
used is recorded in `AgriAdvisoryPerformance.deliveryMode` (inherited from
`AgriDigitalPerformance`).

---

## Non-Goals

- **Pricing** — handled by `ServiceOffer.pricingModel` and Beckn core `Price`.
- **Eligibility criteria** — handled by `ServiceOffer.eligibilityCriteria`.
- **Bulk discount terms** — handled by `ServiceOffer.bulkDiscountAvailable`.
- **Cancellation policy** — handled by `ServiceOffer.cancellationPolicies`.
- **Content quality or accuracy SLAs** — not in scope for this schema; use `serviceNotes`
  in `ServicePerformance` or a separate SLA attachment.

---

## Upstream Candidates

The following fields may be proposed for upstream inclusion in future versions of
`ServiceOffer` in `generic-service` if they prove reusable across domains:

- `deliveryChannels` — applicable to any digital service with channel-specific delivery.
- `languageOptions` — applicable to any service delivered in multiple languages.
- `subscriptionPeriodDays` — applicable to subscription-based service offers generally.
