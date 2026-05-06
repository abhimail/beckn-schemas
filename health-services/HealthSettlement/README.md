# HealthSettlement Schema

**Container:** `Settlement.settlementAttributes`
**Extends:** `ServiceSettlement/v2.1`
**Protocol Version:** 2.0
**Semantic Model:** generalised
**Use Cases:** UC0 bulk procurement, UC1 single patient engagement, UC2 camp engagement
**Tag:** health health-service settlement

## Overview

HealthSettlement captures payment settlement details for health service engagements on the ONHS network. It inherits the full ServiceSettlement field set — receipt confirmation, adjustment type, dispute tracking — and adds three health-specific fields that close the financial loop on the procurement and camp models: entitlement traceability, credit-back unit count, and camp cash ledger linkage.

## Attachment Points

Attaches to `Settlement.settlementAttributes` inside `Contract.settlements[]`. Populated via `on_status` messages after the Provider NP confirms payment receipt. For UC2 camp engagements, the settlement is updated at end-of-camp reconciliation with on-actuals adjustment data.

## Design Rationale

- **`entitlementRef` on Settlement** — When an engagement is funded by entitlement drawdown, the settlement record carries the HealthEntitlement ID that was decremented. This provides a traceable link from the individual settlement event back to the procurement contract — important for financial reconciliation, audit, and dispute resolution at the network level.

- **`entitlementCreditBack`** — In UC2 camp engagements, if fewer patients were screened than committed (`confirmedPatients < committedPatients`), the undelivered units must be credited back to the HealthEntitlement's `remainingCapacity`. `entitlementCreditBack` records the exact integer count of units returned, making the capacity accounting explicit and auditable. The Provider NP is responsible for updating the HealthEntitlement's capacity counters via an `update` message referencing this value.

- **`campLedgerRef`** — For UC2 camps with field cash collection, the settlement record links to the camp cash ledger maintained by the implementing agency. This allows the agency to reconcile field-collected cash against the settled network transaction without merging two separate financial systems.

- **On-actuals reconciliation flow** — The full UC2 settlement sequence uses `adjustmentType: ON_ACTUALS`, `adjustmentAmount` (negative credit for undelivered units), `entitlementCreditBack` (units returned), and `finalSettlementRef` (post-adjustment transaction reference). All fields except `entitlementCreditBack` and `campLedgerRef` are inherited from ServiceSettlement.

## Non-Goals

- Does not model the financial transaction itself (gateway, bank transfer) — that is the responsibility of the payment gateway and is referenced via `receiptRef` / `finalSettlementRef`.
- Does not model pricing terms — those belong in HealthConsideration.
- Does not model the entitlement capacity state — those belong in HealthEntitlement.

## Upstream Candidates

- `entitlementRef` on Settlement — the pattern of linking a settlement record back to the entitlement that funded it is applicable to any domain with procurement-funded consumption (education vouchers, government welfare schemes, corporate benefit programmes). Could be generalised in ServiceSettlement.
- `entitlementCreditBack` — the explicit unit credit-back count for under-delivery reconciliation is applicable to any bulk-commitment domain. Could be generalised in ServiceSettlement as `capacityCreditBack`.
