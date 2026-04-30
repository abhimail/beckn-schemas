# HealthResource — v2.1

**Schema Pack Version:** 2.1.0
**Released:** April 2026
**Network:** ONHS
**Status:** Initial release

### Container

- **Resource.resourceAttributes**

### Key features

- Health service type discriminator (5 types)
- Six service units: ANALYSIS, CONSULTATION, SCREENING, REPORT, SESSION, TEST
- Clinical validation object (accreditation body, registration number, specialty, validity)
- `servicePrerequisites` array — health-generic "what to bring / have ready" field:
  - Types: DEVICE / DOCUMENT / PHYSICAL_CONDITION / SAMPLE / REFERRAL / OTHER
  - Covers AI analysis (audio samples), teleconsultation (camera/internet), lab tests (fasting), physical consultations (referral), etc.
- `analyticsEngineSpecs` — conditionally required for DIAGNOSTIC_ANALYTICS:
  - Model name, version, confidence threshold, input formats, regulatory approval

### Design note on servicePrerequisites

`servicePrerequisites` replaces the original `input_specs` concept. Framing it as
"prerequisites to avail the service" makes it health-generic: the structure accommodates
device requirements, document requirements, physical conditions, and sample collection
instructions equally well across all health service types.
