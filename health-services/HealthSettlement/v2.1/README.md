# HealthSettlement — v2.1

**Schema Pack Version:** 2.1.0
**Released:** April 2026
**Network:** ONHS
**Status:** Initial release

### Container

- **Settlement.settlementAttributes**

### Key features

- Full ServiceSettlement v2.2 feature set (receipt, adjustment type, partial completion, dispute)
- `entitlementRef` — traces settlement to the originating procurement entitlement
- `entitlementCreditBack` — units credited back to the entitlement after on-actuals reconciliation
- `campLedgerRef` — links to the field cash collection ledger for UC2 camps

### On-actuals camp reconciliation (UC2)

At end-of-camp:
1. `adjustmentType` = ON_ACTUALS
2. `partialCompletionFraction` = actual patients / committed patients
3. `adjustmentAmount` = negative value (credit/refund for undelivered units)
4. `entitlementCreditBack` = units returned to the HealthEntitlement's `remainingCapacity`
5. `finalSettlementRef` records the final settled transaction
