# AgriCommodityPriceResource Schema

**Container:** `Resource.resourceAttributes`
**Protocol Version:** 2.0
**Semantic Model:** generalised
**Use Cases:** UC3 — Commodity Price (mandi/APMC price feeds, modal price data, arrival volumes, price trend advisories, futures price data)
**Tag:** agri-advisory resource commodity-price

---

## Overview

`AgriCommodityPriceResource` models a commodity market information service capability that a
Provider NP (market intelligence platform, government data aggregator, commodity exchange)
exposes for discovery and procurement by Seeker NPs (government agencies, NGOs, FPOs,
farmer collectives).

A resource of this type describes which commodities and markets it covers, the types of price
data it delivers (spot prices, modal prices, arrival volumes, futures prices, price trends,
price forecasts), how frequently it updates, and whether it provides interpreted trading advice.
Actual price data is delivered out-of-band (app, API feed, SMS) once a contract is in place.

This schema extends `AgriServiceResource` (from the `agri-services-ext` pack), which extends
`ServiceResource` from the `generic-service` pack. Inherited fields include:

- `coverageAreaCodes` — machine-filterable geographic scope (LGD district/state codes for India)
- `languagesSupported` — BCP 47 language codes for farmer-facing content
- `serviceCategory` — typically `DIGITAL_ADVISORY`
- `providerType` — typically `MARKET_INFO_SERVICE`

---

## Attachment Points

| Field | Location in Beckn message |
|---|---|
| `resourceAttributes` | `catalog.resources[n].resourceAttributes` |
| Schema context | `context.schemaContext[]` entry referencing this schema's context.jsonld |

---

## Design Rationale

### Why `commodities` and `marketCodes` as CodedValue arrays?

Commodity classification and market registries are maintained by multiple authorities
(AGROVOC for crops, Agmarknet/APMC for markets, NCDEX/MCX for exchange-traded commodities).
A CodedValue with `@context` pointing to the authority URI allows each provider to reference
the appropriate registry without constraining the schema to a single vocabulary. This is
particularly important for inter-state and cross-network interoperability where market code
registries vary by state.

### Why `priceDataTypes` as a fixed enum (unlike `weatherParameters`)?

Unlike meteorological parameters (which number in the hundreds and reference authoritative
external standards), commodity price data types form a small, stable, domain-defined set
that changes infrequently. A fixed enum provides unambiguous semantics for Seeker NP
filtering without the overhead of an external vocabulary reference. New types (e.g.
`EXPORT_PARITY_PRICE`) can be added to the schema by amendment rather than requiring a
separate vocabulary authority.

### Why `includesTradingAdvice` as a boolean flag?

Advisory services that include trading recommendations (e.g. "sell now", "hold for 2 weeks")
are subject to different regulatory requirements in India than pure data services. The boolean
flag allows Seeker NPs to filter out or specifically seek advisory services that cross the
data-to-recommendation boundary, and enables Provider NPs to make a compliance-relevant
declaration in their resource metadata.

---

## Non-Goals

- This schema does NOT model the price data payload format (JSON time series, CSV, XML).
  Delivery format is negotiated in the contract.
- This schema does NOT define commodity or market codes. It references external authorities
  (AGROVOC, Agmarknet, NCDEX) via the CodedValue `@context` field.
- This schema does NOT cover grain exchange or futures contract specifications. FUTURES_PRICE
  in `priceDataTypes` indicates availability of futures price data, not contract modelling.
- This schema does NOT cover crop insurance premium pricing or government MSP (Minimum Support
  Price) advisory. Those would require separate resource schemas.

---

## Upstream Candidates

- `dataSourceRef` — equivalent single-source reference also appears in `AgriWeatherResource`.
  A common `primaryDataSourceRef` at `AgriServiceResource` level should be evaluated.
- `priceUpdateFrequencyHours` — equivalent to `advisoryUpdateFrequencyHours`
  (AgriCropAdvisoryResource) and `updateFrequencyHours` (AgriWeatherResource). A harmonised
  `contentUpdateFrequencyHours` at `AgriServiceResource` level is recommended for the next
  schema review cycle.
