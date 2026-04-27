# SchemeSettlement Schema

**Container:** `Settlement.settlementAttributes`
**Protocol Version:** 2.0
**Semantic Model:** generalised
**Use Cases:** Government benefit disbursement recording, PFMS transaction tracking, multi-installment DBT settlement, crop insurance claim settlement
**Tag:** agri-schemes scheme-discovery government-welfare settlementAttributes

---

## Overview

`SchemeSettlement` is a **new** v2.1 schema (no v2 equivalent). It extends
`Settlement.settlementAttributes` with the details of an actual benefit disbursement event:
the disbursement date, amount actually disbursed, currency, government transaction reference
(PFMS ID), installment number, total installments, and the discharge channel (NEFT/RTGS/etc.).

In v2, all of this was crammed into the `DisbursementRecord` sub-schema inside
`SchemeOrderAttributes.sor:disbursementRecord`. The v2.1 Settlement model cleanly expresses
multi-installment disbursement: one `Consideration` captures the total annual obligation;
one `Settlement` object is created per installment tranche.

Migrated fields: `sor:disbursementDate`, `sor:disbursedAmount`, `sor:disbursedCurrency`,
`sor:governmentTransactionReference`, `sor:disbursementInstallment`, `sor:totalInstallments`
(from SchemeOrderAttributes) + `sfa:disbursementMode` (from SchemeFulfillmentAttributes).

---

## Attachment Points

| Container | Schema | Rationale |
|-----------|--------|-----------|
| `Settlement.settlementAttributes` | `SchemeSettlement` | Each disbursement tranche is a separate Settlement event — date, amount, PFMS reference, and installment number. Multiple Settlement objects per Consideration support PM-KISAN's 3-installment structure. |

---

## Design Rationale

### 1. One Settlement per installment
Multi-installment schemes (PM-KISAN: 3 × ₹2,000/year; some housing schemes: construction
milestone-linked tranches) are now first-class. Each installment = one Settlement object,
linked to one Consideration. Previously this required custom array logic inside
`sor:disbursementRecord`, which had no natural way to express partial disbursements.

### 2. disbursementMode migrated from SchemePerformance
In v2, `sfa:disbursementMode` (NEFT/RTGS/CHEQUE) was in fulfillmentAttributes because there
was nowhere better. In v2.1, it correctly describes the discharge channel for the settlement —
how the money physically moves to the beneficiary's account.

### 3. PFMS reference as settlementRef
The government transaction reference (PFMS ID, DBT reference, insurance claim settlement
number) is the primary audit/reconciliation identifier. It maps naturally to
`Settlement.settlementRef` in core, extended here with additional Indian government-specific
detail.

---

## Non-Goals

- **No committed obligation amount.** Total agreed benefit (e.g., ₹6,000/year) belongs in `SchemeConsideration`.
- **No application process.** Submission modes and agent details are in `SchemePerformance`.
- **No scheme content.** Scheme descriptions are in `SchemeResource`.
