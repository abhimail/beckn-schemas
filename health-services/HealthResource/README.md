# HealthResource Schema

**Container:** `Resource.resourceAttributes`
**Extends:** `ServiceResource/v2.1`
**Protocol Version:** 2.0
**Semantic Model:** generalised
**Use Cases:** UC0 bulk procurement, UC1 single patient engagement, UC2 camp engagement
**Tag:** health health-service resource

## Overview

HealthResource captures the health-specific intrinsic attributes of a health service resource on the ONHS network. It extends ServiceResource with a health service type discriminator, clinical validation credentials, service prerequisites, and analytics engine specifications for AI-driven diagnostic services.

A HealthResource describes *what a service is and what it requires* — not how it is priced, booked, or delivered. All of those concerns belong in HealthOffer, HealthContract, and HealthPerformance respectively.

## Attachment Points

Attaches to `Resource.resourceAttributes`. Published in the Provider NP's catalog as part of `on_discover` responses. The `healthServiceType` field in HealthResource drives which fields are conditionally required in HealthContract, HealthPerformance, and HealthConsideration at transaction time.

## Design Rationale

- **`healthServiceType` on Resource, not Contract** — The service type is an intrinsic property of the resource (a cough analysis service is always DIAGNOSTIC_ANALYTICS regardless of who books it). Placing it on the Resource allows Seekers to filter by service type at discovery time without opening a contract. HealthContract carries a copy as a discriminator for runtime conditional validation.

- **`servicePrerequisites` over `input_specs`** — Framing prerequisites as "what the patient or field worker must have ready" makes the field health-generic: a cough analysis needs an audio sample (SAMPLE), a teleconsultation needs a device with camera (DEVICE), a lab test may need fasting (PHYSICAL_CONDITION), a specialist consultation may need a referral letter (REFERRAL). A single array with a typed enum covers all cases without per-service-type branching.

- **`analyticsEngineSpecs` as a conditional sub-object** — AI-driven services have metadata (model name, version, confidence threshold, input format, regulatory approval) that is irrelevant to human-delivered services. Grouping these in a single conditional sub-object rather than scattering them as top-level optional fields keeps the schema clean for non-AI service types.

- **`clinicalValidation` as a Resource attribute** — Accreditation and registration credentials are properties of the resource (the practitioner or the AI model) that remain stable across bookings. Placing them here enables discovery-time filtering by credential type without requiring a contract to be initiated.

## Non-Goals

- Does not model pricing or commercial terms — those belong in HealthOffer and HealthConsideration.
- Does not model appointment scheduling policies — those are in ServiceResource (base) and HealthOffer.
- Does not model patient consent — that is captured in HealthContract at booking time.
- Does not model the clinical report or output artefacts — those are in HealthPerformance.

## Upstream Candidates

- `servicePrerequisites` (typed prerequisite array with DEVICE / DOCUMENT / PHYSICAL_CONDITION / SAMPLE / REFERRAL / OTHER) — applicable to any professional service domain where the client must prepare before availing the service. Generic enough for Beckn core or the generic-service base pack.
- `clinicalValidation` pattern (accreditation body, registration number, specialty, validity date) — the structure is generic credential validation applicable to any regulated professional service (legal, financial, educational). Could be generalised as a `credentialValidation` type in the generic-service base.
