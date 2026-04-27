# SchemeContract Schema

**Container:** `Contract.contractAttributes`
**Protocol Version:** 2.0
**Semantic Model:** generalised
**Use Cases:** Agriculture scheme application order, government enrollment confirmation, UC2 shadow tracking order for external enrollments
**Tag:** agri-schemes scheme-discovery government-welfare contractAttributes

---

## Overview

`SchemeContract` extends `Contract.contractAttributes` with transaction-level metadata for a
confirmed scheme application: the official government application reference, scheme authority
status, consent records (DPDP Act 2023), and — for UC2 — the external enrollment reference
that links a Beckn tracking contract to a pre-existing government enrollment.

Migrated from: `SchemeOrderAttributes` (v2, `orderAttributes` container). Prefix changed from
`sor:` to `scr:`. The `DisbursementRecord` sub-schema has been dissolved: disbursement amounts
move to `SchemeConsideration`, and disbursement transaction records move to `SchemeSettlement`.

---

## Attachment Points

| Container | Schema | Rationale |
|-----------|--------|-----------|
| `Contract.contractAttributes` | `SchemeContract` | Transaction-level government reference IDs, scheme outcome status, consent timestamps, and external enrollment references are contract-level metadata spanning the full contract lifecycle. |

---

## Design Rationale

### 1. Three-party contracts as a v2.1 design win
Scheme contracts in this domain are genuinely multi-party:
- **UC1 (Agent-Assisted):** APPLICANT + SCHEME_AUTHORITY + FIELD_AGENT — three participant roles.
- **UC2 (Status Enquiry):** BENEFICIARY + SCHEME_AUTHORITY + PORTAL_OPERATOR — the external
  portal system that originally enrolled the beneficiary becomes a named party in the Beckn
  tracking contract.

The v2.1 `Contract.participants[]` array captures this naturally. v2's Order.provider +
Order.billing was restricted to a binary buyer–seller pattern.

### 2. disbursementRecord dissolved
In v2, `sor:disbursementRecord` was a blob in `orderAttributes`. In v2.1, the record is split:
- Promised benefit amount → `SchemeConsideration.considerationAttributes` (scr counterpart:
  `Consideration.considerationAttributes`)
- Actual disbursement tranche → `SchemeSettlement.settlementAttributes` (one Settlement per
  installment). This makes multi-installment PM-KISAN disbursements (3 × ₹2,000/year) first-class.

### 3. UC2 external enrollment reference stays at contract level
`scr:externalEnrollmentRef` identifies the entire contract's external counterpart — the government
enrollment ID used to create a Beckn tracking contract against an existing enrollment. This is
a contract-level concept (the whole contract links to one external enrollment), not a per-commitment
attribute.

### 4. Consent fields at contract level
`scr:applicantConsentGiven` and `scr:consentTimestamp` record DPDP Act 2023 consent at the
contract level — consent is given once per application, not per commitment.

---

## Non-Goals

- **No disbursement amounts.** Committed benefit amount belongs in `SchemeConsideration`.
- **No disbursement transaction records.** PFMS references and installment tracking are in `SchemeSettlement`.
- **No execution mechanics.** Application submission mode and agent assignment are in `SchemePerformance`.
- **No eligibility policy.** Who can apply is modelled in `SchemeOffer`.

---

## Upstream Candidates

None. Fields are specific to Indian government scheme administration (DPDP Act consent fields,
external enrollment reference formats). However, the general pattern of `externalEnrollmentRef` +
`externalEnrollmentIdType` is reusable for any UC2 shadow-order pattern in government networks.
