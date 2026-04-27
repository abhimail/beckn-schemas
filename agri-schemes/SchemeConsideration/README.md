# SchemeConsideration Schema

**Container:** `Consideration.considerationAttributes`
**Protocol Version:** 2.0
**Semantic Model:** generalised
**Use Cases:** Government scheme benefit obligation modelling, agreed benefit amount per application, multi-installment scheme consideration tracking
**Tag:** agri-schemes scheme-discovery government-welfare considerationAttributes

---

## Overview

`SchemeConsideration` is a **new** v2.1 schema (no v2 equivalent). It extends
`Consideration.considerationAttributes` with the government's committed obligation per scheme
application — the agreed benefit type, amount, and period. This is the "promise" layer:
the government agrees to provide a specific benefit to the beneficiary.

The actual discharge of that promise (the individual disbursement tranches, PFMS transaction
references, installment numbers) is recorded in `SchemeSettlement.settlementAttributes`.

In v2, this information was crammed into `SchemeOrderAttributes.sor:disbursementRecord`.
The v2.1 Consideration/Settlement split makes multi-installment schemes (e.g., PM-KISAN:
3 × ₹2,000/year) architecturally clean: one Consideration capturing the ₹6,000/year promise,
three Settlement objects recording the actual disbursements.

---

## Attachment Points

| Container | Schema | Rationale |
|-----------|--------|-----------|
| `Consideration.considerationAttributes` | `SchemeConsideration` | The government's committed benefit obligation per application — what they promise to provide (type, amount, period). Separate from the actual disbursement record (SchemeSettlement). |

---

## Design Rationale

### 1. Consideration ≠ disbursement
In government schemes, the "consideration" flows from government to beneficiary (not the
reverse). The Consideration object captures the committed obligation: what the government
has agreed to provide and in what form. This is distinct from the v2 `Offer.benefitQuantum`
(catalogue-time "up to" declaration) and from `SchemeSettlement` (the actual disbursement event).

### 2. Multi-installment support
PM-KISAN and similar installment-based DBT schemes can now be modelled with a single
Consideration (total annual obligation: ₹6,000) and multiple Settlement objects (one per
installment of ₹2,000). This was impossible in v2 without bespoke array logic inside
`orderAttributes`.

### 3. Benefit type from Offer, not re-specified
`sco:benefitType` mirrors the `sof:benefitType` from the corresponding offer but is recorded
at the consideration level to confirm the agreed benefit category for this specific application.

---

## Non-Goals

- **No disbursement transaction details.** PFMS references and disbursement dates belong in `SchemeSettlement`.
- **No eligibility criteria.** Who qualifies is modelled in `SchemeOffer`.
- **No catalogue amounts.** The "up to" declarative amount is in `SchemeOffer.sof:benefitQuantum.sof:monetaryAmount`.
