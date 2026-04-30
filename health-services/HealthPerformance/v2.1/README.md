# HealthPerformance — v2.1

**Schema Pack Version:** 2.1.0
**Released:** April 2026
**Network:** ONHS
**Status:** Initial release

### Container

- **Performance.performanceAttributes**

### Key features

- Appointment window and confirmed time
- Service location (required for PHYSICAL_CONSULTATION and LAB_TEST)
- Dual completion confirmation (provider + client)
- `followupRecommendationCode` (NONE / ROUTINE / SOON / URGENT / EMERGENCY) — health-generic urgency signal
- `provisionalDiagnosis` — applies to DIAGNOSTIC_ANALYTICS, TELECONSULTATION, PHYSICAL_CONSULTATION
- `artifactsGenerated` — array of Document labels in Descriptor.docs[] (reports, prescriptions, recordings)
- `deletionAttestation` — compliance record confirming raw patient data deletion
- `clinicalInterpretation` — conditionally required for DIAGNOSTIC_ANALYTICS:
  - Confidence score, flagged findings, model output reference
  - Specialist review tracking

### Conditional requirements

| healthServiceType | Additional required fields |
|---|---|
| DIAGNOSTIC_ANALYTICS | clinicalInterpretation, artifactsGenerated |
| PHYSICAL_CONSULTATION | serviceLocation |
| LAB_TEST | serviceLocation |
