# SchemeContract — v2.1

**Schema Pack Version:** 2.1.0
**Released:** April 2026
**Status:** Initial release

## Notes

Initial release of the SchemeContract schema targeting the Beckn v2.1 generalised model.
Migrated from SchemeOrderAttributes (v2, orderAttributes container).

Key changes from v2:
- Container renamed: `orderAttributes` → `contractAttributes`
- Schema renamed: `SchemeOrderAttributes` → `SchemeContract`
- Prefix renamed: `sor:` → `scr:`
- IRI base updated: `https://schema.beckn.io/SchemeOrderAttributes#` → `https://schema.beckn.io/SchemeContract#`
- `DisbursementRecord` sub-schema removed from this schema:
  - Amount fields → `SchemeConsideration.considerationAttributes` (sco:)
  - Transaction/installment fields → `SchemeSettlement.settlementAttributes` (sse:)
- context.jsonld is now fully self-contained (no `@import` from core)
- Added `html` and `html_detail` Handlebars templates to renderer.json
