# Agriculture Advisory Domain Reference

> Domain tag: `advisory:agri`
> Previously `advisory:uki` in v1/Gen1 Beckn implementations
> Generated schema pack: `agri-advisory/` (6 top-level schemas)

---

## Sub-Use-Case Breakdown

The agriculture advisory domain has three distinct sub-use cases, each with different item, offer,
and fulfillment semantics:

| Sub-Use Case | UC Code | Nature | Order Lifecycle |
|---|---|---|---|
| Crop/Disease Advisory | UC1 | Free and paid digital knowledge content | Search → (Select) → (Order) for paid |
| Commodity Price Listing | UC2 | Market price data discovery (no order) | Search only (no transactional flow) |
| Weather Forecast Data | UC3 | Paid weather intelligence product | Full: Search → Select → Init → Confirm → Status → Cancel |

---

## Schema Pack Structure

Six top-level schemas were generated, organized by container:

| Schema | Container | Applies To | Namespace |
|---|---|---|---|
| `CropAdvisoryItemAttributes` | `itemAttributes` | UC1 | `caia:` |
| `CommodityPriceItemAttributes` | `itemAttributes` | UC2 | `cpia:` |
| `WeatherForecastItemAttributes` | `itemAttributes` | UC3 | `wfia:` |
| `AgriAdvisoryOfferAttributes` | `offerAttributes` | UC1 + UC3 | `aaoa:` |
| `CommodityMarketOfferAttributes` | `offerAttributes` | UC2 | `cmoa:` |
| `AgriAdvisoryFulfillmentAttributes` | `fulfillmentAttributes` | UC1 + UC2 + UC3 | `aafa:` |

---

## v1 → v2 Field Migration Table

### UC1 — Crop/Disease Advisory

| v1 Field / Tag | v2 Location | Notes |
|---|---|---|
| `context.domain = "advisory:uki"` | `context.domain = "advisory:agri"` | Domain code updated |
| `item.tags[category.code]` = `disease-control` | `CropAdvisoryItemAttributes.advisoryCategory` = `DISEASE_CONTROL` | Promoted to typed enum |
| `item.tags[languages]` = `["en","mr"]` | `CropAdvisoryItemAttributes.languages` | First-class array |
| `item.tags[crop-details.crop-name]` | `CropAdvisoryItemAttributes.cropContext.cropName` | Nested sub-schema |
| `item.tags[crop-details.variety]` | `CropAdvisoryItemAttributes.cropContext.cropVariety` | |
| `item.tags[crop-details.plantation-date]` | `CropAdvisoryItemAttributes.cropContext.plantationDate` | ISO 8601 |
| `item.tags[crop-details.growth-stage]` | `CropAdvisoryItemAttributes.cropContext.growthStage` | Typed enum |
| `item.tags[crop-details.soil-type]` | `CropAdvisoryItemAttributes.cropContext.soilType` | |
| `item.tags[crop-details.irrigation-type]` | `CropAdvisoryItemAttributes.cropContext.irrigationType` | |
| `item.tags[crop-details.disease-name]` | `CropAdvisoryItemAttributes.cropContext.diseaseName` | |
| `item.tags[environment]` | Removed | Environmental context was ambient; not core to item identity |
| `item.media[].url` + `mimetype` | `CropAdvisoryItemAttributes.contentUrl` + `contentMimeType` | |
| `item.media[].mimetype` enum | `CropAdvisoryItemAttributes.contentType` (TEXT/VIDEO/PDF/AUDIO/…) | Typed enum |
| `intent.tags[crop-details]` | `fulfillmentAttributes.targetLocation` + item filtering | Search intent params move to fulfillment or catalog filter |
| `fulfillment.type = "HOME_DELIVERY"` | `fulfillment.mode = "DIGITAL"` | Digital delivery mode |
| `order.cancellation_terms` | `AgriAdvisoryOfferAttributes.cancellationPolicy` | Structured sub-schema |

### UC2 — Commodity Price Listing

| v1 Field | v2 Location | Notes |
|---|---|---|
| `item.descriptor.name` = commodity name | `CommodityPriceItemAttributes.commodityName` | |
| `item.tags[commodity-details.variety]` | `CommodityPriceItemAttributes.commodityVariety` | |
| `item.tags[commodity-details.grade]` | `CommodityPriceItemAttributes.commodityGrade` | |
| `item.price.minimum_value` | `CommodityMarketOfferAttributes.minPrice` | **Critical migration**: price range moves from Item to Offer |
| `item.price.maximum_value` | `CommodityMarketOfferAttributes.maxPrice` | |
| `item.price.estimated_value` | `CommodityMarketOfferAttributes.averagePrice` + core `beckn:price` | Core price = representative/modal |
| `item.price.currency` | `CommodityMarketOfferAttributes.currency` | |
| `item.tags[unit-of-measure]` | `CommodityMarketOfferAttributes.unitOfMeasure` | Moves to Offer |
| `fulfillment.stops[0].location.gps` | `AgriAdvisoryFulfillmentAttributes.targetLocation.geo` | GeoJSON Point |
| `intent.tags[price-date-range]` | `AgriAdvisoryFulfillmentAttributes.priceQueryTimeRange` | Time range moves to fulfillment |
| `intent.tags[radius]` | `AgriAdvisoryFulfillmentAttributes.targetRegionRadiusKm` | Numeric, km unit |
| `context.timestamp` used as observation time | `CommodityPriceItemAttributes.priceObservationPeriod` | Explicit observation period |
| AGMARKNET arrivals data (implicit) | `CommodityMarketOfferAttributes.arrivals` | New field in v2 |

### UC3 — Weather Forecast Data

| v1 Field | v2 Location | Notes |
|---|---|---|
| `item.descriptor.name` = forecast product name | `item.descriptor.name` (core) + `WeatherForecastItemAttributes.forecastType` | |
| `item.tags[forecast-type]` | `WeatherForecastItemAttributes.forecastType` (enum) | |
| `item.tags[forecast-duration]` | `WeatherForecastItemAttributes.forecastDurationDays` + `.forecastDurationISO` | Both numeric and ISO 8601 |
| `item.tags[data-points]` | `WeatherForecastItemAttributes.weatherDataPoints` (array) | Strongly-typed enum array |
| `item.tags[output-formats]` | `WeatherForecastItemAttributes.outputFormats` | Typed enum array |
| `item.price.value` | core `beckn:price` (PriceSpecification) | Unchanged |
| `fulfillment.stops[0].location.gps` | `AgriAdvisoryFulfillmentAttributes.targetLocation.geo` | GeoJSON Point |
| `fulfillment.type = "HOME_DELIVERY"` | `fulfillment.mode = "DIGITAL"` | |
| `order.cancellation_terms` | `AgriAdvisoryOfferAttributes.cancellationPolicy` | |
| `on_status` fulfillment URL | `AgriAdvisoryFulfillmentAttributes.contentAccessUrl` | Post-delivery access URL |
| `on_cancel` refund logic | `AgriAdvisoryOfferAttributes.cancellationPolicy.refundPercentage` | |

---

## Key Design Decisions

### 1. Split Offer Schemas for UC1+UC3 vs UC2
UC1 and UC3 both sell digital content (advisories and weather forecasts) → `AgriAdvisoryOfferAttributes`
with pricing model (FREE/PAID/FREEMIUM/SUBSCRIPTION), access type, and cancellation policy.

UC2 is pure price discovery (not a transaction) → `CommodityMarketOfferAttributes` with
statistical price range (min/max/average). The two use cases have fundamentally different
commercial semantics so they warranted separate Offer schemas.

### 2. Price Range Belongs on Offer, Not Item (UC2)
In v1, `item.price.minimum_value/maximum_value/estimated_value` all lived on the Item.
In v2 this violates the principle that Item carries intrinsic attributes and Offer carries
commercial policies. The price range (min/max/average mandi prices) is a commercial observation,
so it was moved entirely to `CommodityMarketOfferAttributes`. Core `beckn:price` on the Offer
carries the single representative (modal) price for discoverability.

### 3. Shared Fulfillment Schema Across All Three Use Cases
All three use cases use DIGITAL fulfillment only (no physical logistics). A single shared
`AgriAdvisoryFulfillmentAttributes` schema was created with optional fields covering:
- `targetLocation` + `targetRegionRadiusKm` — UC2 (price discovery radius) and UC3 (weather forecast point)
- `contentAccessUrl` / `contentAccessExpiry` — UC1 and UC3 (post-delivery content link)
- `priceQueryTimeRange` — UC2 (observation date range filter)
- `requestedLanguage` — all UCs

This avoids schema proliferation while keeping the Fulfillment container focused on execution metadata.

### 4. Intent Search Parameters Become Typed Attributes
v1 used `intent.tags[crop-details]` as unstructured key-value pairs for search filtering.
In v2, these become first-class typed properties on `CropAdvisoryItemAttributes.cropContext`
(a structured sub-schema). This enables proper catalog indexing, filtering, and validation.

### 5. UC2 Has No Order Lifecycle
Commodity price listing is informational only — there is no `select → init → confirm` flow.
Consumers search the catalog and read prices. The item and offer schemas are present but no
`orderAttributes` schema was generated.

### 6. CropContext as Optional Sub-Schema
Crop context (crop name, variety, growth stage, soil type, irrigation type, disease name)
was modeled as an optional nested sub-schema `CropContext` within `CropAdvisoryItemAttributes`.
This groups related contextual fields that may be populated for personalized advisories
but are optional for generic catalog items.

---

## Key Item Attributes Per Sub-Use Case

### UC1 — CropAdvisoryItemAttributes
- `advisoryCategory`: `DISEASE_CONTROL | SPRAY_SCHEDULE | PEST_FORECAST | GENERAL_ADVISORY`
- `contentType`: `TEXT | VIDEO | PDF | AUDIO | INFOGRAPHIC | INTERACTIVE`
- `contentMimeType`: IANA MIME type
- `contentUrl`: URI (may be access-gated for paid content)
- `languages`: ISO 639-1 codes (array)
- `targetCrops`: common/scientific crop names (array)
- `targetDiseases`: disease/pest names (array)
- `applicableGrowthStages`: enum array (`SOWING` through `POST_HARVEST`)
- `cropContext`: `{cropName, cropVariety, plantationDate, growthStage, soilType, irrigationType, diseaseName}`
- `advisorySource`: originating organization
- `expertCredentials`: `{expertName, institution, qualification}`

### UC2 — CommodityPriceItemAttributes
- `commodityName`: common commodity name
- `commodityCode`: AGMARKNET/FAOSTAT code
- `commodityVariety`: cultivar/variety
- `commodityGrade`: quality grade
- `commoditySize`: physical size descriptor
- `unitOfMeasure`: price unit (per Quintal, per Kg, etc.)
- `mandiName`: APMC/mandi market name
- `mandiCode`: official market code
- `priceObservationPeriod`: `{startDate, endDate}` — observation time window
- `priceSource`: AGMARKNET, e-NAM, NHB, etc.
- `dataLicense`: GODL, CC-BY, etc.

### UC3 — WeatherForecastItemAttributes
- `forecastType`: `WEATHER_FORECAST | SEASONAL_OUTLOOK | AGRO_ADVISORY | HISTORICAL_DATA | CLIMATE_RISK`
- `forecastDurationDays`: integer
- `forecastDurationISO`: ISO 8601 duration (e.g., `P14D`)
- `forecastResolution`: `HYPERLOCAL | VILLAGE | BLOCK | DISTRICT | STATE | NATIONAL`
- `weatherDataPoints`: array of 17 meteorological parameters
- `outputFormats`: array of `PDF | JSON_API | CSV | SMS | PUSH_NOTIFICATION | IN_APP_DISPLAY | EMAIL_REPORT`
- `providerLicense`: `OPEN | PROPRIETARY | GOVERNMENT | CREATIVE_COMMONS | ACADEMIC`
- `modelSource`: IMD, ECMWF, GFS, proprietary, etc.
- `updateFrequency`: ISO 8601 duration (e.g., `PT6H`)
- `accreditedBy`: regulatory/accreditation body

---

## Offer Attributes Per Sub-Use Case

### UC1 + UC3 — AgriAdvisoryOfferAttributes
- `pricingModel`: `FREE | PAID | FREEMIUM | SUBSCRIPTION`
- `accessType`: `OPEN_ACCESS | ONE_TIME_PURCHASE | SUBSCRIPTION_ACCESS | API_KEY_ACCESS`
- `contentLicense`: `ALL_RIGHTS_RESERVED | CC_BY | CC_BY_NC | CC_BY_SA | OPEN_GOVERNMENT | PROPRIETARY`
- `accessValidityPeriod`: `{durationISO, endDate}`
- `cancellationPolicy`: `{isRefundable, refundWindowHours, refundPercentage, cancellationReasons}`
- `trialAvailable`: boolean
- `maxActiveOrders`: integer

### UC2 — CommodityMarketOfferAttributes
- `minPrice`: minimum observed price
- `maxPrice`: maximum observed price
- `averagePrice`: average/modal price (maps to `estimated_value` in v1)
- `currency`: ISO 4217
- `unitOfMeasure`: per Quintal, per Kg, etc.
- `priceVolatilityIndicator`: `LOW | MODERATE | HIGH | VERY_HIGH`
- `arrivals`: `{quantity, unit}` — mandi arrivals volume

---

## Shared Fulfillment Attributes (All UCs)

### AgriAdvisoryFulfillmentAttributes (container: `fulfillmentAttributes`)
- `deliveryMode`: `DIGITAL_LINK | API_RESPONSE | PDF_DOWNLOAD | SMS | PUSH_NOTIFICATION | IN_APP_DISPLAY | EMAIL_ATTACHMENT`
- `targetLocation`: GeoJSON object (Point or Polygon) — farm GPS or mandi region
- `targetRegionRadiusKm`: search radius in km (UC2)
- `requestedLanguage`: ISO 639-1
- `contentAccessUrl`: post-fulfillment content URI
- `contentAccessExpiry`: access link expiry date-time
- `deliveryConfirmation`: BPP-issued confirmation reference
- `priceQueryTimeRange`: `{startDate, endDate}` (UC2 date filter)

---

## Upstream Candidates

The following attributes are generic enough to be candidates for promotion to the Beckn v2 core:

| Attribute | Current Schema | Rationale for Upstream |
|---|---|---|
| `languages` (array of ISO 639-1 codes) | `CropAdvisoryItemAttributes`, `CommodityPriceItemAttributes`, `WeatherForecastItemAttributes` | Applies to any digital content item in any domain |
| `contentUrl` | `CropAdvisoryItemAttributes` + `AgriAdvisoryFulfillmentAttributes` | Generic for any digital content delivery |
| `contentMimeType` | `CropAdvisoryItemAttributes` | Applicable to any digital media item |
| `accessValidityPeriod` | `AgriAdvisoryOfferAttributes` | Useful for any time-limited digital access offer |
| `cancellationPolicy` sub-schema | `AgriAdvisoryOfferAttributes` | Generic commercial pattern applicable to all digital service offers |
| `priceVolatilityIndicator` | `CommodityMarketOfferAttributes` | Useful for any commodity or financial product domain |
| `deliveryConfirmation` | `AgriAdvisoryFulfillmentAttributes` | Generic digital delivery receipt pattern |

---

## Non-Goals

- Physical logistics (no warehouse, vehicle, or delivery tracking)
- Payment gateway integration (handled by core `beckn:Payment`)
- User profile or farm profile storage
- IoT sensor data feeds (real-time streams; only packaged forecast products)
- Subsidy or government scheme eligibility (India-specific regulatory data excluded)
- Multi-language content bundles (each item = one primary language)
- Agri-input marketplace (seeds/fertilizers/pesticides = different domain, closer to ONDC retail)
