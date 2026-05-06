# HealthConsideration Schema

**Container:** `Consideration.considerationAttributes`
**Extends:** `ServiceConsideration/v2.1`
**Protocol Version:** 2.0
**Semantic Model:** generalised
**Use Cases:** UC0 bulk procurement, UC1 single patient engagement, UC2 camp engagement
**Tag:** health health-service consideration

## Overview

HealthConsideration captures pricing and payment terms for health service engagements on the ONHS network. It inherits the full ServiceConsideration field set — unit pricing, payment methods, payer archetype, milestone payment schedules, and the fresh-payment / entitlement-drawdown bifurcation rule — and adds two health-specific fields for UC2 camp billing: per-patient unit amount and camp cash collection reference.

## Attachment Points

Attaches to `Consideration.considerationAttributes` inside `Contract.consideration[]`. Published as a DRAFT (proposed pricing) in `on_discover` catalog responses with no payment fields present. Updated to QUOTED at `on_init` preview. Finalised to ACTIVE at `on_confirm` with exactly one of `paymentAuthorisation` or `entitlementRef` present.

## Design Rationale

- **Funding bifurcation as a network invariant** — Every ONHS consumption engagement is funded by exactly one mechanism: a fresh payment gateway authorisation (`paymentAuthorisation`) or a drawdown against a pre-purchased HealthEntitlement (`entitlementRef`). The `oneOf` constraint in ServiceConsideration (inherited here) enforces this invariant at schema validation time. The two fields are mutually exclusive and, at contract confirmation, exactly one must be present.

- **Three-state `oneOf`** — At catalogue time (status: DRAFT) and init preview (status: QUOTED), neither payment field is present — the Consideration is a pricing proposal. The `oneOf` includes a "draft/proposed" branch that explicitly permits this state, ensuring catalogue-time payloads pass validation. See ServiceConsideration for the full lifecycle explanation.

- **`perPatientAmount` for UC2 on-actuals billing** — In camp engagements, the total consideration is calculated as `confirmedPatients × perPatientAmount` at end-of-camp reconciliation, not at booking time. Storing the per-patient rate separately from the total makes the reconciliation arithmetic explicit and auditable. The Provider NP uses this field alongside `campCommitment.confirmedPatients` on the HealthEntitlement to calculate the final settlement adjustment (`confirmedPatients × perPatientAmount`).

- **`campCashCollectionRef` for field collection** — In camp settings where patients pay individually at the venue (UC2 pay-at-counter), field workers collect cash on behalf of the implementing agency. `campCashCollectionRef` links the contract's consideration to the field cash ledger maintained by the implementing agency, providing an audit trail without requiring real-time payment gateway integration in low-connectivity environments.

## Non-Goals

- Does not model payment settlement or receipt confirmation — those belong in HealthSettlement.
- Does not model the entitlement capacity, validity, or drawdown rules — those belong in HealthEntitlement.
- Does not model cancellation refund policies — those belong in HealthOffer.

## Upstream Candidates

- `perPatientAmount` — the pattern of storing a per-unit rate separately from the total for post-completion reconciliation is applicable to any bulk service engagement where quantity is not fixed at booking time. Could be generalised in ServiceConsideration as `perUnitRateForReconciliation`.
- `campCashCollectionRef` / field cash ledger linkage — applicable to any domain with field-based, low-connectivity payment collection (agricultural services, rural education, community health). Could be generalised in ServiceConsideration as `fieldCollectionRef`.
