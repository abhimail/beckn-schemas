# AgriWeatherResource Schema

**Container:** `Resource.resourceAttributes`
**Protocol Version:** 2.0
**Semantic Model:** generalised
**Use Cases:** UC2 — Weather Forecast (agro-meteorological forecasts, nowcasts, interpreted agro advisories delivered to farmers and Seeker NPs)
**Tag:** agri-advisory resource weather

---

## Overview

`AgriWeatherResource` models a meteorological data service capability that a Provider NP
(weather data provider, national meteorological service, or agro-met platform) exposes for
discovery and procurement by Seeker NPs.

A resource of this type describes the forecast horizon, temporal resolution, spatial resolution,
the meteorological parameters available, the upstream data source, and whether the provider can
interpret raw forecasts into agro-advisory outputs (e.g. "ideal sowing window this week",
"frost risk alert — protect nursery seedlings"). The actual forecast data or advisory messages
are delivered out-of-band once a contract is in place.

This schema extends `AgriServiceResource` (from the `agri-services-ext` pack), which extends
`ServiceResource` from the `generic-service` pack. Inherited fields include:

- `coverageAreaCodes` — machine-filterable geographic scope (county/district codes)
- `languagesSupported` — BCP 47 language codes for farmer-facing output
- `serviceCategory` — typically `DIGITAL_ADVISORY`
- `providerType` — typically `WEATHER_DATA_PROVIDER`

---

## Attachment Points

| Field | Location in Beckn message |
|---|---|
| `resourceAttributes` | `catalog.resources[n].resourceAttributes` |
| Schema context | `context.schemaContext[]` entry referencing this schema's context.jsonld |

---

## Design Rationale

### Why `weatherParameters` as CodedValue rather than an enum?

Meteorological parameter vocabularies (WMO BUFR, CF Conventions) are authoritative, versioned
external standards with hundreds of defined parameters. Constraining this schema to a fixed enum
would either over-constrain (excluding valid parameters from CF Conventions) or require constant
schema updates as new parameters gain relevance. Using CodedValue with `@context` pointing to
the authority URI allows each provider to declare exactly which parameters they serve, using
the authoritative code, without schema changes.

### Why separate `forecastHorizonDays` and `forecastResolutionHours`?

These are orthogonal capabilities: a provider might offer 7-day forecasts at 24-hour resolution,
or 3-day forecasts at 3-hour resolution. Seeker NPs with precision agriculture use cases need
fine temporal resolution; government scheme planners may only need daily summaries. Separating
these allows independent filtering.

### Why `supportsAgroAdvisory` as a boolean flag?

This is a discovery-critical binary: a raw weather data provider and an interpreted
agro-advisory service are fundamentally different procurement targets. Seeker NPs seeking
farmer-ready advisory messages cannot substitute a raw data feed, and vice versa. The boolean
avoids over-engineering a capability taxonomy at this stage of network maturity.

### Why East Africa context for the example?

The agri advisory network covers both India and East Africa. The weather schema is particularly
relevant for East Africa where meteorological services (Kenya Meteorological Department,
IGAD Climate Prediction and Applications Centre) play a critical role in smallholder farming
advisory. East Africa is used for this schema's example to demonstrate multi-geography coverage.

---

## Non-Goals

- This schema does NOT model the forecast data payload format (NetCDF, GRIB, JSON time series).
  That is a delivery-layer specification negotiated in the contract.
- This schema does NOT enumerate specific WMO BUFR or CF Convention parameter codes. The
  `weatherParameters` CodedValue references the external authority.
- This schema does NOT model satellite imagery products, soil moisture remote sensing, or
  vegetation index data. Those would require a separate resource schema.

---

## Upstream Candidates

- `updateFrequencyHours` — equivalent to `advisoryUpdateFrequencyHours` in
  `AgriCropAdvisoryResource` and `priceUpdateFrequencyHours` in `AgriCommodityPriceResource`.
  A harmonised `contentUpdateFrequencyHours` at `AgriServiceResource` level should be evaluated
  in the next schema review cycle to reduce cross-schema duplication.
- `dataSourceRef` — appears in both `AgriWeatherResource` and `AgriCommodityPriceResource`.
  A common `primaryDataSourceRef` at `AgriServiceResource` level, with
  `AgriCropAdvisoryResource.dataSourceRefs` as an array variant, is worth evaluating.
