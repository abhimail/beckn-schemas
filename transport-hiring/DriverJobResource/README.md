# DriverJobResource Schema

**Container:** `Resource.resourceAttributes`
**Protocol Version:** 2.0
**Semantic Model:** generalised
**Use Cases:** UC1 — Driver/Aggregator Initiated Job Application
**Tag:** transport-hiring hiring resource

## Overview

DriverJobResource captures the extension attributes for a driver job vacancy published
by a transport operator platform (bus company, logistics firm, cab aggregator, etc.).
It extends the generic `HiringJobResource` with fields specific to the transport hiring
vertical: driver role classification, required vehicle categories, credential and training
requirements, and an operator reputation capsule.

All generic job fields (job title, job type, work mode, location, shift type, working hours,
contract duration, experience requirements, skills, application deadline) are inherited from
`HiringJobResource` and are not redefined here.

## Attachment Points

| Container | Schema | Reason |
|-----------|--------|--------|
| `beckn:resourceAttributes` | `DriverJobResource` | Driver-specific job vacancy metadata extending the generic hiring resource |

The schema does not attach to `offerAttributes`, `contractAttributes`, or
`performanceAttributes` — commercial terms (salary, benefits package) belong to
`HiringJobOffer` / `TransportHiringOffer`, and contract execution (onboarding,
assignment) belongs to `TransportHiringPerformance`.

## Design Rationale

**Extend, don't duplicate.** All generic hiring attributes live in `HiringJobResource`.
Only fields that have no meaning outside the transport driver context are placed here.
This allows a Seeker NP to discover and filter driver jobs using the base hiring
discovery schema while still surfacing domain-specific facets (role_type,
vehicle_categories_required) as primary filter dimensions.

**`required_credentials` and `required_training` at Resource level.** These are
intrinsic to the job vacancy — they describe what the job requires, not what a
specific offer's terms are. They are safe to expose at discovery stage without
PII concerns.

**`benefits_summary` at Resource level.** High-level benefit labels (PF, ESI, etc.)
are discovery-stage signals. Detailed benefits package belongs in `offerAttributes`.

**`operator_reputation`** is a discovery-stage trust signal inherited from the base
`HiringJobResource`. It is not redefined here; the driver context uses it as-is.

## Non-Goals

- Does not model salary, compensation, or benefits detail (those belong in `offerAttributes`)
- Does not model application or onboarding workflow (belongs in `contractAttributes` / `performanceAttributes`)
- Does not model candidate-side attributes (see `DriverCandidateProfileResource`)
- Does not model vehicle-specific route or schedule details (those are operational, not hiring)
- Does not carry any PII — identity of the hiring entity is at `beckn:provider` level

## Upstream Candidates

The following properties may be generic enough to promote to `HiringJobResource` base
if other hiring verticals (healthcare, construction, gig economy) need the same concepts:

- `required_credentials` (as a generic `credentialType[]` field)
- `required_training` (as a generic `trainingRequirement[]` field)
- `benefits_summary` (already present in some base hiring schemas)
