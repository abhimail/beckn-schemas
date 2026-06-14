# HealthReferral Schema

**Container:** `Contract.contractAttributes`
**Extends:** `ServiceCoordination/v2.1`
**Protocol Version:** 2.0
**Semantic Model:** generalised
**Use Cases:** UC4 clinical referral (T1 coordination contract)
**Tags:** health, referral, contract

## Overview

HealthReferral is the clinical referral contract (T1) for a Beckn health referral network. It
extends the generic `ServiceCoordination` with a clinical narrowing of
`targetCriteria` (specialty / sub-specialty / equipment / procedure /
consultationModality), structured clinical `consent` with a `consentClass` (A/B/C),
a `referralNote` that specialises the generic `handoverDocument`, government scheme
membership (`schemeRef`), a clinical urgency tier, and two health-specific lifecycle
states and deviation codes.

The coordinator (care coordinator) is discovered via the **generic**
`ServiceCoordinationResource` — there is no health-specific coordination
Resource/Offer.

## Attachment points

- **Primary:** `Contract.contractAttributes` in `on_confirm` / `on_status` of the
  T1 referral-coordination transaction.

## Design rationale

- **`targetCriteria` clinical narrowing** — adds clinical specialty / sub-specialty
  (self-owned CodedValues), equipment and procedure needs, and consultation modality
  to the generic criteria. Required within a HealthReferral.
- **`consent` + `consentClass`** — reuses the `HealthContract.consent` field set as
  its base and adds the A/B/C class with class-specific fields: `mediatorCredentialRef`
  (A), `originatingConsentRef` (B), `deemedBasisCode` + `clinicalJustification` +
  `ratifiedAt` (C).
- **`referralNote`** specialises `ServiceCoordination.handoverDocument` — it inherits
  the credential-scope / access-window / revocation reference semantics and adds the
  clinical header (specialty, urgency, prior result links). The clinical body is never
  inline; `artifactRef` resolves to a Document in `Descriptor.docs[]` (§4).
- **Health lifecycle states** add `SCHEME_PREAUTH_PENDING` and
  `POST_FACTO_CONSENT_PENDING`; **health deviation codes** add `CONSENT_WITHDRAWN` and
  `ELIGIBILITY_EXPIRED`.

## Document reference resolution (§4)

`referralNote.artifactRef` and `consent.consentDocRef` carry **label strings**, not
URLs. Each label resolves to a Beckn core `Document` in the contract envelope's
`Descriptor.docs[]`, which carries the actual `url` (+ `mimeType`, `standard`). The
worked example demonstrates this: `referralnote-001` resolves to the cardiology
referral-note Document.

## Non-goals

- The downstream booking (T2) — belongs in `HealthContract` (via `coordinationRef`).
- Execution / attendance / outcome — belongs in `HealthPerformance`.
- Coordinator standing capability / terms — belong in the generic
  `ServiceCoordinationResource` / `ServiceCoordinationOffer`.

## Upstream candidates

- ServiceCoordination (generic coordination contract)
- ServiceContract (generic Beckn service contract)

## Coded values

Self-owned coded fields (`consent.consentClass`, `targetCriteria.specialty`/`subSpecialty`, and `deviation.reasonCode` — reused from `ServiceCoordination`) use the pinned typed-`CodedValue` pattern. The referral-facing deviation vocabulary maps to the generic `ServiceCoordination` codes via `skos:exactMatch`. Resolution and extension follow **the CodedValue resolution & extension convention (RFC-001, draft)**.
