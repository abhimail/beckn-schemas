# SchemeResource Schema

**Container:** `Resource.resourceAttributes`
**Protocol Version:** 2.0
**Semantic Model:** generalised
**Use Cases:** Agriculture and government welfare scheme discovery, NGO programme cataloguing, rural beneficiary scheme search
**Tag:** agri-schemes scheme-discovery government-welfare resourceAttributes

---

## Overview

`SchemeResource` is the extension schema that adds domain-specific intrinsic metadata to a
Beckn v2.1 `Resource` representing a government or NGO welfare scheme. It describes **what the
scheme is** — its type, funding model, sponsoring authority, required documents, and the
benefit categories it covers — rather than who can apply (→ `SchemeOffer`) or how it is
delivered (→ `SchemePerformance`).

This schema supports the Agriculture/Government Scheme Discovery network where farmers and rural
beneficiaries discover applicable welfare schemes across multiple providers — central government,
state governments, district bodies, and NGOs — through a single Beckn-enabled application.

Migrated from: `SchemeItemAttributes` (v2, `itemAttributes` container). Prefix changed from
`sia:` to `sr:` to match the v2.1 generalised naming convention.

---

## Attachment Points

| Container | Schema | Rationale |
|-----------|--------|-----------|
| `Resource.resourceAttributes` | `SchemeResource` | Intrinsic identity, type, documentation, and application channels of the scheme as a discoverable resource — independent of who can apply or how it is delivered. |

Sub-schemas (`RequiredDocument`, `SchemeBenefitSummary`) are co-located in `v2.1/attributes.yaml`
and do not get separate folders — they are referenced only from within `SchemeResource`.

---

## Design Rationale

### 1. Eligibility lives in Offer, not Resource
Eligibility criteria (age, gender, caste, income, land ownership) are commercial access policy —
they determine who gets the offer. In v2.1 terms, eligibility is a `SchemeOffer.offerAttributes`
concern. The resource (scheme) is neutral; the offer wrapping it carries the access conditions.

### 2. Benefit quantum lives in Offer and Consideration, not Resource
The monetary or coverage amount (₹5 lakh health cover, 100 employment days) is an offer-time
descriptor in `SchemeOffer.offerAttributes.sof:benefitQuantum`. The transactional committed
amount lives in `SchemeConsideration.considerationAttributes`. The resource schema carries only
descriptive benefit summaries (`sr:schemeBenefits`) with no amounts, so any offer wrapping this
resource may express its own quantum.

### 3. Scheme type and funding model are required
These two fields drive the primary discovery filters. A seeker cannot meaningfully compare
schemes without knowing whether a scheme is insurance vs. DBT vs. employment, or whether it is
centrally-sponsored vs. state vs. NGO-funded. They are `required` in this schema.

### 4. Application modes support multi-channel discovery
Rural India has diverse digital literacy levels. Surfacing application modes (online, offline,
agent-assisted, CSC) at the resource level lets BAP applications filter and present options
appropriate to the beneficiary's capability — without touching offer or performance layers.

### 5. Official scheme code for cross-referencing
Government schemes carry official codes (e.g., `PM000024` for Central Sector Schemes). These
enable interoperability with DigiLocker, PFMS, and scheme aggregator portals.

---

## Non-Goals

- **No applicant PII.** Applicant profile data (name, Aadhaar, income) is collected via
  `xinput` / `Form` at the offer/performance stage.
- **No monetary amounts.** Benefit coverage amounts belong in `SchemeOffer` and `SchemeConsideration`.
- **No eligibility rules.** Who can apply is modelled in `SchemeOffer.offerAttributes`.
- **No fulfillment state machine.** Application status tracking is in `SchemePerformance`.
- **No customizations.** Schemes are atomic resources with no variants or bundles.

---

## Upstream Candidates

| Attribute | Rationale |
|-----------|-----------|
| `sr:availableLanguages` | Any content resource could declare its language availability; applicable to education, health advisory, and other welfare verticals globally. |
| `sr:applicationModes` | A generalised "access channel" concept applicable to any service or entitlement vertical — permits, licences, grants. |
| `sr:officialPortalUrl` | A generic "canonical reference URL" is broadly useful for any institutional product or public-sector catalogue. |
