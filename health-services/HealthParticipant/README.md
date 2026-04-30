# HealthParticipant Schema

**Container:** `Participant.participantAttributes`
**Extends:** *(standalone — no generic-service base)*
**Protocol Version:** 2.0
**Semantic Model:** generalised
**Use Cases:** UC1 single patient engagement, UC2 camp engagement
**Tag:** health health-service participant

## Overview

HealthParticipant captures health-specific participant attributes for individuals and organisations involved in a health service contract on the ONHS network. It models six distinct roles — PATIENT, CARE_GIVER, SPECIALIST, FIELD_WORKER, PAYER, IMPLEMENTING_AGENCY — with role-appropriate identity, credential, and payer detail sub-objects.

Unlike other Health* schemas, HealthParticipant has no generic-service base to extend. Participant attributes are health-network-specific enough that a generic-service base would add no reusable value.

## Attachment Points

Attaches to `Participant.participantAttributes` within `Contract.participants[]`. Each participant entry in the contract carries a `role` and the role-appropriate attributes. Multiple participants may appear in a single contract (e.g. PATIENT + FIELD_WORKER in a UC1 engagement; PATIENT + CARE_GIVER + SPECIALIST in a teleconsultation).

## Design Rationale

- **Six typed roles rather than a flat attribute bag** — Health contracts involve a varied cast of participants with fundamentally different attribute needs. Typing roles explicitly and making role-specific sub-objects conditionally required (specialistAccreditation for SPECIALIST, payerDetails for PAYER) prevents implementers from populating irrelevant fields and makes validation meaningful.

- **ABHA as the patient identity anchor** — The Ayushman Bharat Health Account (ABHA) ID is India's national health identifier. Surfacing it as a top-level field (rather than burying it in a generic identifier array) makes it directly filterable and linkable to the national health stack. The field is optional because not all ONHS deployments will operate within the ABHA ecosystem, and international deployments may substitute a different national health identifier.

- **`specialistAccreditation` mirroring `clinicalValidation` on HealthResource** — The same credential structure (accreditation body, registration number, specialty, validity) appears both on the Resource (the service unit) and on the participant playing the SPECIALIST role. At Resource level it describes the service capability; at Participant level it identifies the individual practitioner delivering a specific engagement. Both are needed: the Resource credential is discovery-time, the Participant credential is contract-time.

- **`payerDetails` for institutional payers** — When `payerArchetype` in HealthConsideration is GOVERNMENT, INSURANCE, or NGO, the contract should identify the paying organisation by name, ID, and scheme reference. `payerDetails` on the PAYER participant provides this without polluting the Consideration schema with identity fields.

- **`primaryLanguage` on FIELD_WORKER** — Field workers operate in specific regional languages. Surfacing the field worker's primary language enables the Provider NP to route AI-generated reports and instructions to the appropriate language version, and supports post-hoc quality analysis of outcomes by language coverage.

## Non-Goals

- Does not model the clinical credentials of the resource/service — those belong in HealthResource (`clinicalValidation`).
- Does not model the payer's financial terms or payment authorisation — those belong in HealthConsideration.
- Does not model consent given by the patient — that belongs in HealthContract.
- Does not model organisational hierarchy or reporting relationships between participants.

## Upstream Candidates

- Typed participant role pattern with role-conditional sub-objects — the structure of declaring a `role` enum and making sub-objects conditionally required by role is applicable to any multi-party domain (legal services: CLIENT / COUNSEL / JUDGE; education: STUDENT / INSTRUCTOR / GUARDIAN; financial services: BORROWER / GUARANTOR / LENDER). Could be generalised as a `participantAttributes` base schema in the generic-service pack.
- `specialistAccreditation` / `credentialValidation` structure — as noted under HealthResource, the accreditation body + registration number + specialty + validity structure is domain-neutral and could be promoted to a shared type.
