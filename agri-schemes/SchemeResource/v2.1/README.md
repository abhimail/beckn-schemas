# SchemeResource — v2.1

**Schema Pack Version:** 2.1.0
**Released:** April 2026
**Status:** Initial release

## Notes

Initial release of the SchemeResource schema targeting the Beckn v2.1 generalised model.
Migrated from SchemeItemAttributes (v2, itemAttributes container).

Key changes from v2:
- Container renamed: `itemAttributes` → `resourceAttributes`
- Schema renamed: `SchemeItemAttributes` → `SchemeResource`
- Prefix renamed: `sia:` → `sr:`
- IRI base updated: `https://schema.beckn.io/SchemeItemAttributes#` → `https://schema.beckn.io/SchemeResource#`
- context.jsonld is now fully self-contained (no `@import` from core)
- Added `protocol_version: "2.0"` and `semantic_model: "generalised"` to profile.json
- Added `html` and `html_detail` Handlebars templates to renderer.json
