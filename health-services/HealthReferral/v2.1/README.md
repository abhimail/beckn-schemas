# HealthReferral — v2.1

**Schema Pack Version:** 2.1.0
**Released:** June 2026
**Use Case:** Patient Referral (UC4) — health referral network
**Status:** under-review

## Notes

The clinical referral contract (T1). Extends `ServiceCoordination/v2.1`. Prefix `hrf:`.

### Container

- **Contract.contractAttributes**

### lifecycleState

Generic `ServiceCoordination` states plus two health-specific:
`SCHEME_PREAUTH_PENDING`, `POST_FACTO_CONSENT_PENDING`.

Conditional requireds (each a separate `allOf[]` if/then):

| When lifecycleState == | then required |
|---|---|
| SCHEME_PREAUTH_PENDING | schemeRef |
| POST_FACTO_CONSENT_PENDING | consent |

### Key fields

- `targetCriteria` (required) — clinical narrowing: specialty / subSpecialty (CodedValue),
  equipmentNeeds, procedureNeeds, consultationModality (IN_PERSON / TELECONSULT)
- `consent` — clinical consent + `consentClass` (A/B/C CodedValue) and class fields
- `referralNote` — specialises generic `handoverDocument`; clinical header + prior result links
- `schemeRef` — government scheme membership (CodedValue, e.g. PMJAY)
- `clinicalUrgencyTier` — ROUTINE / URGENT / EMERGENCY (plain enum)
- `deviation.reasonCode` — generic codes plus CONSENT_WITHDRAWN, ELIGIBILITY_EXPIRED

### Worked example

`examples/example-cardiology-referral.json` — complete on_confirm T1 contract for the
Dr. Priya → Dr. Mehta cardiology referral, including `descriptor.docs[]` carrying the
actual referral-note Document that `referralNote.artifactRef` resolves to.
