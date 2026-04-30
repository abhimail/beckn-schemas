# HealthConsideration — v2.1

**Schema Pack Version:** 2.1.0
**Released:** April 2026
**Network:** ONHS
**Status:** Initial release

### Container

- **Consideration.considerationAttributes**

### Key features

- Full ServiceConsideration v2.2 feature set (pricing, payment methods, payer archetype, milestone schedule)
- Network-wide bifurcation rule enforced as `oneOf`: exactly one of `paymentAuthorisation` or `entitlementRef`
- `perPatientAmount` for UC2 camp per-head billing
- `campCashCollectionRef` for field cash ledger tracking in UC2

### Bifurcation rule

Every ONHS consumption engagement is funded by exactly one of:
- `paymentAuthorisation` — fresh payment (pay-at-counter, direct payment, NEFT)
- `entitlementRef` — drawdown against a HealthEntitlement issued at UC0

This is a network invariant. Both fields must never appear together and at least one must be present.
