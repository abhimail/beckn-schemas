# HealthParticipant Schema

**Container:** `Participant.participantAttributes`
**Extends:** `ServiceParticipant/v2.1`
**Protocol Version:** 2.0
**Semantic Model:** generalised
**Use Cases:** UC1 single patient engagement, UC2 camp engagement
**Tag:** health health-service participant

## Overview

HealthParticipant captures health-specific participant attributes for individuals and organisations involved in a health service contract on the ONHS network. It models six distinct roles — PATIENT, CARE_GIVER, SPECIALIST, FIELD_WORKER, PAYER, IMPLEMENTING_AGENCY — with role-appropriate identity, credential, and payer detail sub-objects.

HealthParticipant extends ServiceParticipant to inherit `credentialRefs`, the generic runtime credential proof array, and adds health-specific fields on top via `allOf`.

## Attachment Points

Attaches to `Participant.participantAttributes` within `Contract.participants[]`. Each participant entry in the contract carries a `role` and the role-appropriate attributes. Multiple participants may appear in a single contract (e.g. PATIENT + FIELD_WORKER in a UC1 engagement; PATIENT + CARE_GIVER + SPECIALIST in a teleconsultation).

## Design Rationale

- **Six typed roles rather than a flat attribute bag** — Health contracts involve a varied cast of participants with fundamentally different attribute needs. Typing roles explicitly and making role-specific sub-objects conditionally required (e.g. specialistAccreditation for SPECIALIST) prevents implementers from populating irrelevant fields and makes validation meaningful.

- **`healthIds` as a generic health identifier array** — Rather than surfacing a single ABHA ID (India-specific, patient-scoped), HealthParticipant models health-sector identifiers as an array of `{system, value}` pairs. The `system` field names the registry (ABHA, NMC, HFR, NPI, GMC, NHS, ASHA-ID, State-HID-KA, NGO-REG) and the `value` carries the identifier within that registry. This covers all six participant roles across geographies: a PATIENT may carry an ABHA or NHS number; a SPECIALIST carries an NMC or NPI registration; a FIELD_WORKER carries an ASHA ID; a PAYER carries an insurer registration. The issuing authority need not be national — state registries, professional councils, and facility registries are equally valid systems. The array is optional and can hold multiple identifiers when a participant is registered in more than one system.

- **`specialistAccreditation` mirroring `clinicalValidation` on HealthResource** — The same credential structure (accreditation body, registration number, specialty, validity) appears both on the Resource (the service unit) and on the participant playing the SPECIALIST role. At Resource level it describes the service capability; at Participant level it identifies the individual practitioner delivering a specific engagement. Both are needed: the Resource credential is discovery-time, the Participant credential is contract-time. Note the distinction between `specialistAccreditation` and `credentialRefs`: the former is structured, query-friendly metadata modelled explicitly for filtering and audit; the latter is the cryptographic or documentary proof (a W3C VC or PDF link) that backs the claim. Both should be present for SPECIALIST participants in regulated deployments.

- **`credentialRefs` inherited from ServiceParticipant** — Runtime credential proof for any participant role. A SPECIALIST attaches their signed W3C Verifiable Credential from the NMC; an IMPLEMENTING_AGENCY attaches their NGO registration document (Beckn Document/2.0 with `standard: "NGORegistration"`); a FIELD_WORKER attaches their ASHA ID card image (`standard: "ASHAIdentityCard"`). Beckn Credential/2.0 is a `oneOf`: the W3C VC branch is an opaque JSON object (Beckn does not validate internal VC structure — the W3C VC Data Model governs that); the Document branch is a Beckn Document/2.0 requiring `label`, `url`, and `mimeType`, with the optional `standard` field carrying the credential type string. This covers both regulated professional contexts (machine-verifiable VCs) and low-infrastructure field deployments (PDF or image document references).

- **PAYER identity via `healthIds` and `Participant.descriptor`** — A PAYER participant's identity is fully expressed by `healthIds` (e.g. `{system: "PMJAY", value: "KA-SCHEME-2023-001"}`, `{system: "IRDAI", value: "..."}`) for registry IDs, and by `Participant.descriptor.name` in the Beckn core for the display name. Payer type (SELF / GOVERNMENT / INSURANCE / NGO) is captured by `payerArchetype` in HealthConsideration, where it belongs alongside the financial terms. A dedicated `payerDetails` sub-object was considered but removed — it duplicated `payerArchetype` (type), `Participant.descriptor.name` (name), and `healthIds` (IDs and scheme codes) without adding any new information.

- **`primaryLanguage` on FIELD_WORKER** — Field workers operate in specific regional languages. Surfacing the field worker's primary language enables the Provider NP to route AI-generated reports and instructions to the appropriate language version, and supports post-hoc quality analysis of outcomes by language coverage.

## Non-Goals

- Does not model the clinical credentials of the resource/service — those belong in HealthResource (`clinicalValidation`).
- Does not model the payer's financial terms or payment authorisation — those belong in HealthConsideration.
- Does not model consent given by the patient — that belongs in HealthContract.
- Does not model payer type or financial terms — payer type belongs in `payerArchetype` in HealthConsideration; payer identity belongs in `Participant.descriptor` and `healthIds`.
- Does not model organisational hierarchy or reporting relationships between participants.

## Upstream Candidates

- Typed participant role pattern with role-conditional sub-objects — the structure of declaring a `role` enum and making sub-objects conditionally required by role is applicable to any multi-party domain (legal services: CLIENT / COUNSEL / JUDGE; education: STUDENT / INSTRUCTOR / GUARDIAN; financial services: BORROWER / GUARANTOR / LENDER). Could be generalised as a `participantRole` field in the ServiceParticipant base.
- `healthIds` (`{system, value}` identifier array) — the generic health identifier pattern is applicable to any regulated domain where participants carry multiple sector-specific IDs. Could be generalised in ServiceParticipant as a `sectorIds` array.
- `specialistAccreditation` / `credentialValidation` structure — the accreditation body + registration number + specialty + validity structure is domain-neutral and could be promoted to a shared `AccreditationRecord` type usable across health, legal, and education domains.
