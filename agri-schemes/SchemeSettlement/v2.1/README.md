# SchemeSettlement — v2.1

**Schema Pack Version:** 2.1.0
**Released:** April 2026
**Status:** Initial release

## Notes

Initial release of the SchemeSettlement schema. This is a **new schema** introduced in v2.1
with no direct v2 equivalent. Fields were extracted from two v2 schemas:

From `SchemeOrderAttributes.DisbursementRecord` (v2):
- `sor:disbursementDate` → `sse:disbursementDate`
- `sor:disbursedAmount` → `sse:disbursedAmount`
- `sor:disbursedCurrency` → `sse:disbursedCurrency`
- `sor:governmentTransactionReference` → `sse:governmentTransactionReference`
- `sor:disbursementInstallment` → `sse:disbursementInstallment`
- `sor:totalInstallments` → `sse:totalInstallments`

From `SchemeFulfillmentAttributes` (v2):
- `sfa:disbursementMode` → `sse:disbursementMode`
