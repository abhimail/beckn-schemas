# SchemePerformance — v2.1

**Schema Pack Version:** 2.1.0
**Released:** April 2026
**Status:** Initial release

## Notes

Initial release of the SchemePerformance schema targeting the Beckn v2.1 generalised model.
Migrated from SchemeFulfillmentAttributes (v2, fulfillmentAttributes container).

Key changes from v2:
- Container renamed: `fulfillmentAttributes` → `performanceAttributes`
- Schema renamed: `SchemeFulfillmentAttributes` → `SchemePerformance`
- Prefix renamed: `sfa:` → `spe:`
- IRI base updated: `https://schema.beckn.io/SchemeFulfillmentAttributes#` → `https://schema.beckn.io/SchemePerformance#`
- `sfa:disbursementMode` field removed — moved to `SchemeSettlement.settlementAttributes` (sse:disbursementMode)
- context.jsonld is now fully self-contained (no `@import` from core)
- Added `html` and `html_detail` Handlebars templates to renderer.json
