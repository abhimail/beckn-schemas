# AgriServiceResource — v2.1

**Schema Pack Version:** 2.1.0
**Released:** May 2026
**Status:** Initial release

## Notes

Initial release of the AgriServiceResource schema targeting the v2.1 generalised model.

This version introduces:
- `serviceCategory` enum covering VACCINATION, BROODING, INCUBATION, AGRI_INPUT, ADVISORY, SCREENING, and DIGITAL_ADVISORY
- `providerType` enum covering VET, AGROVET, EXTENSION_OFFICER, AGRI_INPUT_DEALER, AGRI_TRAINER, DIGITAL_ADVISORY_PLATFORM, WEATHER_DATA_PROVIDER, and MARKET_INFO_SERVICE
- `livestockTypes` array allowing multi-species resources
- `serviceAreaHierarchy` sub-schema capturing village/ward/county/country coverage with optional radius
- `coverageAreaCodes` array for coded administrative area references (LGD, ISO 3166-2, etc.)

### Container

- **Resource.resourceAttributes**

### Key Features

- Agriculture service categories (vaccination, brooding, advisory, digital advisory, etc.)
- Provider types (vet, extension officer, agrovet, digital platform, etc.)
- Livestock type array — a single resource can serve multiple species
- Hierarchical geographic coverage (village, ward, county, country)
- Coded coverage area references for interoperability with LGD, GADM, and similar authorities
- Extends all base ServiceResource fields (serviceUnit, capacity, availability, languages supported)

### Compatibility

- Requires Beckn Protocol core 2.0
- Depends on: `ServiceResource` (allOf), `CodedValue` ($ref for coverageAreaCodes items)
- No breaking changes expected for v2.2; additional service categories and provider types will be added as enum extensions
