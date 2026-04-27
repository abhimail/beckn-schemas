# SchemeOffer Schema

**Container:** `Offer.offerAttributes`
**Protocol Version:** 2.0
**Semantic Model:** generalised
**Use Cases:** Agriculture and government welfare scheme discovery, eligibility-based filtering, benefit quantum declaration
**Tag:** agri-schemes scheme-discovery government-welfare offerAttributes

---

## Overview

`SchemeOffer` is the extension schema that adds eligibility criteria, benefit quantum, and
application window metadata to a Beckn v2.1 `Offer` representing a government or NGO welfare
scheme. It describes **who can apply** and **what they receive** under a specific offer
configuration — covering demographic, economic, professional, identity, educational, and
residency dimensions.

Migrated from: `SchemeOfferAttributes` (v2, `offerAttributes` container). Prefix changed from
`soa:` to `sof:` to match the v2.1 generalised naming convention.

---

## Attachment Points

| Container | Schema | Rationale |
|-----------|--------|-----------|
| `Offer.offerAttributes` | `SchemeOffer` | Eligibility criteria, benefit quantum, application window, and enrollment cap are commercial access-policy properties of the offer, not the underlying scheme resource. |

---

## Design Rationale

### 1. Eligibility as offer policy
All eligibility dimensions (demographic, economic, professional, identity, education, residency)
are access policies that determine who receives the offer. In the v2.1 model, this is correctly
placed in `offerAttributes` — the Offer governs access terms over the Resource.

### 2. Benefit quantum as descriptive offer metadata
`sof:benefitQuantum.sof:monetaryAmount` describes the maximum benefit amount declared in the
scheme offer (e.g., "up to ₹5 lakh per family per year" on a PM-JAY offer). This is a
catalogue-time descriptor. The transactional committed amount per application lives in
`SchemeConsideration.considerationAttributes`. Both coexist without conflict — the offer
declares what is available, the consideration records what was agreed.

### 3. Eligibility form (xinput) reference in offerAttributes
The `sof:eligibilityForm` field carries a URL to a multi-step eligibility questionnaire.
Per Beckn v2.1, xinput-style forms are collected at the offer stage before transacting.
The field is retained in offerAttributes to maintain alignment with the protocol's
form-collection flow.

### 4. Multi-dimensional eligibility for targeting
Rural welfare schemes frequently combine multiple eligibility dimensions (age AND caste AND
income AND state). The structured sub-schema approach (six named sub-objects rather than
free-form tags) makes eligibility filterable, indexable, and machine-comparable across schemes.

---

## Non-Goals

- **No scheme identity.** Scheme name, type, and documentation belong in `SchemeResource`.
- **No fulfillment mechanics.** Application submission modes and agent assignment are in `SchemePerformance`.
- **No transactional amounts.** Committed disbursement amounts are in `SchemeConsideration` and `SchemeSettlement`.
- **No applicant PII at schema level.** Applicant-specific data is supplied as an intent payload, not stored in the schema.

---

## Upstream Candidates

| Attribute | Rationale |
|-----------|-----------|
| `sof:eligibilityCriteria` (generic form) | Multi-dimensional structured eligibility (demographic, economic, professional, residency) is a broadly applicable pattern for any means-tested entitlement globally — social welfare, licensing, grants, scholarships. Strong upstream candidate. |
| `sof:maxBeneficiaries` | A generic "enrollment cap" concept applicable to any capacity-limited offer. |
