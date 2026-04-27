# SchemeOffer — v2.1

**Schema Pack Version:** 2.1.0
**Released:** April 2026
**Status:** Initial release

## Notes

Initial release of the SchemeOffer schema targeting the Beckn v2.1 generalised model.
Migrated from SchemeOfferAttributes (v2, offerAttributes container).

Key changes from v2:
- Schema renamed: `SchemeOfferAttributes` → `SchemeOffer`
- Prefix renamed: `soa:` → `sof:`
- IRI base updated: `https://schema.beckn.io/SchemeOfferAttributes#` → `https://schema.beckn.io/SchemeOffer#`
- Container name `offerAttributes` is unchanged (v2 → v2.1 mapping is identity for Offer)
- context.jsonld is now fully self-contained (no `@import` from core)
- Added `html` and `html_detail` Handlebars templates to renderer.json
- `soa:benefitQuantum.soa:monetaryAmount` retained as catalogue-time descriptor; transactional amount moved to SchemeConsideration
