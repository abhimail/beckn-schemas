# agri-advisory-v21 — Beckn Protocol v2.0.0 LTS Schema Pack

**Version:** 2.1.0
**Status:** Under review
**Protocol:** Beckn Protocol v2.0.0 LTS (Generalised model — Resource/Offer/Contract)

---

## Overview

This schema pack defines the Beckn v2.1 extension schemas for the **Agri Advisory
Network** — a digital public infrastructure network enabling Seeker NPs (government
agencies, NGOs, implementing organisations) to discover and procure digital
agricultural advisory services from Provider NPs (advisory platforms, weather data
services, market intelligence services).

The three use cases covered are:

| UC | Name | Resource type |
|---|---|---|
| UC1 | Crop Advisory | AgriCropAdvisoryResource |
| UC2 | Weather Forecast | AgriWeatherResource |
| UC3 | Commodity Price | AgriCommodityPriceResource |

---

## Schema Inheritance

```
Beckn v2.1 Core
├── ServiceResource          (generic-service)
│   └── AgriServiceResource  (agri-services-ext)
│       ├── AgriCropAdvisoryResource    ← UC1
│       ├── AgriWeatherResource         ← UC2
│       └── AgriCommodityPriceResource  ← UC3
│
├── ServiceOffer             (generic-service)
│   └── AgriAdvisoryOffer               ← all UCs
│
├── ServicePerformance       (generic-service)
│   └── AgriDigitalPerformance  (agri-services-ext)
│       └── AgriAdvisoryPerformance     ← all UCs
│
├── ServiceConsideration     (generic-service) — reused as-is
├── ServiceContract          (generic-service) — reused as-is
├── ServiceParticipant       (generic-service) — reused as-is
├── ServiceEntitlement       (generic-service) — reused as-is
└── ServiceSettlement        (generic-service) — reused as-is

Shared type definitions
└── agri-common/CodedValue/  (re-export of generic-service/generic-common/CodedValue/)
```

---

## Folder Structure

```
agri-advisory-v21/
├── README.md
├── agri-common/
│   └── CodedValue/
│       ├── attributes.yaml   ← re-export of upstream generic-common CodedValue
│       └── README.md
├── AgriCropAdvisoryResource/
│   └── v2.1/attributes.yaml
├── AgriWeatherResource/
│   └── v2.1/attributes.yaml
├── AgriCommodityPriceResource/
│   └── v2.1/attributes.yaml
├── AgriAdvisoryOffer/
│   └── v2.1/attributes.yaml
└── AgriAdvisoryPerformance/
    └── v2.1/attributes.yaml
```

---

## Dependency Packs

This pack references schemas from two sibling packs. Both must be present for
`$ref` resolution:

| Pack | Location | Schemas used |
|---|---|---|
| `generic-service` | `../agri services/generic-service/` | ServiceResource, ServiceOffer, ServicePerformance, ServiceConsideration, ServiceContract, ServiceParticipant, ServiceEntitlement, ServiceSettlement, **generic-common/CodedValue** |
| `agri-services-ext` | `../agri services/agri-services-ext/` | AgriServiceResource, **AgriDigitalPerformance** |

---

## Reused Schemas (no local extension needed)

The following generic-service schemas are used directly in agri advisory contracts
without domain-specific extension:

- **ServiceConsideration** — covers pay-per-engagement (paymentAuthorisation) and
  government bulk procurement (entitlementRef + payerArchetype: GOVERNMENT). Rich
  milestone payment schedule support for advance + completion instalment structures.
- **ServiceContract** — bookingChannel (APP/SMS/WHATSAPP/VOICE) and facilitatorId
  cover all agri advisory booking scenarios.
- **ServiceParticipant** — credentialRefs cover NGO registration, government MOU,
  and FPO registration credentials.
- **ServiceEntitlement** — directly models pre-purchased advisory capacity for
  government scheme bulk procurement. geographyScope + serviceScope constrain
  entitlement redemption to scheme geography and advisory type.
- **ServiceSettlement** — ON_ACTUALS adjustment supports reconciliation where
  committed farmer-advisory units differ from actual deliveries.

---

## Non-Goals

The following are explicitly out of scope for this schema pack:

1. **Physical logistics** — no warehouse management, vehicle routing, or
   last-mile delivery tracking. Advisory services are digital; the network
   does not model physical fulfilment.

2. **Payment gateway integration** — payment authorisation, gateway selection,
   and settlement routing are handled by the Beckn core `ServiceConsideration`
   and `ServiceSettlement` schemas. This pack does not extend or replace those
   mechanisms.

3. **User profile or farm profile storage** — farm size, land records,
   livestock inventory, and farmer identity are not stored in the network.
   Seeker NPs may pass contextual parameters at query time but the network
   does not persist farm profiles.

4. **IoT sensor data feeds** — real-time raw sensor streams (soil moisture
   probes, weather station telemetry) are out of scope. This pack models
   packaged forecast and advisory products derived from such data, not the
   underlying data pipes.

5. **Multi-language content bundles** — each advisory delivery is in one
   primary language. Language preference is negotiated via `requestedLanguage`
   and `deliveredLanguage` fields in `AgriAdvisoryPerformance`; the network
   does not bundle or manage multi-language content variants.

6. **Agri-input marketplace** — seeds, fertilisers, pesticides, and equipment
   are a separate Beckn domain. This pack covers advisory and information
   services only; physical agri-input procurement is out of scope.
