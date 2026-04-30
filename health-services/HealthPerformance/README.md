# HealthPerformance Schema

**Container:** `Performance.performanceAttributes`
**Extends:** `ServicePerformance/v2.1`
**Protocol Version:** 2.0
**Semantic Model:** generalised
**Use Cases:** UC1 single patient engagement, UC2 camp engagement
**Tag:** health health-service performance

## Overview

HealthPerformance captures the clinical execution details of a health service engagement on the ONHS network. It extends ServicePerformance with health-specific fields: clinical interpretation (for AI-driven services), generated artefacts (reports, prescriptions), follow-up urgency coding, provisional diagnosis, and data deletion attestation for regulatory compliance.

HealthPerformance is populated progressively across the engagement lifecycle — appointment details are set at confirm, completion flags are updated during service delivery, and clinical outputs (interpretation, artefacts) are populated when the provider delivers results.

## Attachment Points

Attaches to `Performance.performanceAttributes` inside `Contract.performance[]`. Present in `on_confirm` (with appointment details) and updated via `on_status` messages as the engagement progresses.

## Design Rationale

- **`clinicalInterpretation` as a conditional sub-object** — AI-driven services (DIAGNOSTIC_ANALYTICS) produce machine-readable outputs (confidence score, flagged findings, model output reference) alongside human-readable reports. Grouping these in a dedicated sub-object keeps the schema clean for non-AI service types where this block is absent. Specialist review tracking (`reviewedBySpecialist`, `specialistReviewAt`) is included here because it is a direct follow-on to the AI output.

- **`followupRecommendationCode` as a typed urgency signal** — Rather than a free-text follow-up note, a coded urgency level (NONE / ROUTINE / SOON / URGENT / EMERGENCY) enables the Seeker NP to surface actionable follow-up instructions to the field worker or patient app without parsing clinical text. The code is health-generic — the same enum applies across DIAGNOSTIC_ANALYTICS, TELECONSULTATION, and PHYSICAL_CONSULTATION.

- **`artifactsGenerated` as document labels** — Like `inputArtifacts` in HealthContract, generated artefacts (lab reports, prescriptions, AI output PDFs, recordings) are referenced by label pointing to `Descriptor.docs[]` entries rather than embedded. This keeps performance payloads lean and supports selective access control — different parties may have access to different documents.

- **`deletionAttestation`** — DISHA and health data regulations require providers to attest to the deletion of raw patient data after the retention period. A structured attestation record (timestamp, policy reference, attestedBy) makes this audit-ready without relying on out-of-band communication.

- **`provisionalDiagnosis`** — Applicable across DIAGNOSTIC_ANALYTICS, TELECONSULTATION, and PHYSICAL_CONSULTATION. Kept as a free-text field at this stage rather than a coded diagnosis (ICD-10) to avoid over-specifying the clinical output format, which varies by provider.

## Non-Goals

- Does not model the full clinical report content — reports are referenced as documents in `Descriptor.docs[]`, not embedded in the performance schema.
- Does not model consent — that is captured in HealthContract.
- Does not model payment or settlement — those belong in HealthConsideration and HealthSettlement.
- Does not model participant identity — that belongs in HealthParticipant.

## Upstream Candidates

- `followupRecommendationCode` (typed urgency enum) — applicable to any professional service where the provider needs to signal follow-up urgency to the seeker (e.g. legal advice, financial review). Could be generalised in ServicePerformance as a `recommendationCode`.
- `artifactsGenerated` (labeled document reference array) — applicable to any service that produces output documents. The pattern of referencing `Descriptor.docs[]` by label rather than embedding content is generic enough for the ServicePerformance base.
- `deletionAttestation` — applicable to any domain with regulated data retention obligations (financial services, HR, education). Could be generalised in ServicePerformance or Beckn core.
