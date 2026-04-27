# SchemeConsideration — v2.1

**Schema Pack Version:** 2.1.0
**Released:** April 2026
**Status:** Initial release

## Notes

Initial release of the SchemeConsideration schema. This is a **new schema** introduced in v2.1
with no direct v2 equivalent. It was extracted from the `DisbursementRecord` sub-schema of
`SchemeOrderAttributes` (v2) as part of the Consideration/Settlement split.

The fields in this schema correspond to:
- `sor:disbursementRecord.sor:disbursedAmount` → `sco:agreedAmount` (total obligation, not per installment)
- `sor:disbursementRecord.sor:disbursedCurrency` → `sco:agreedAmountCurrency`
- `sof:benefitQuantum.sof:benefitType` (offer-level declaration) → `sco:benefitType` (confirmed at contract time)
- `sof:benefitQuantum.sof:benefitPeriod` → `sco:benefitPeriod`
