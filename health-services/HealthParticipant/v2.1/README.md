# HealthParticipant — v2.1

**Schema Pack Version:** 2.1.0
**Released:** April 2026
**Network:** ONHS
**Status:** Initial release

### Container

- **Participant.participantAttributes**

### Key features

- Six participant roles: PATIENT, CARE_GIVER, SPECIALIST, FIELD_WORKER, PAYER, IMPLEMENTING_AGENCY
- Generic health identifier array (healthIds) — [{system, value}] pairs covering any health registry across all roles (ABHA, NMC, HFR, NPI, ASHA-ID, etc.)
- Runtime credential proof (credentialRefs) inherited from ServiceParticipant — Beckn Credential/v2.0 array (W3C VC or Document attachment)
- Specialist accreditation object (body, registration number, specialty, validity)
- PAYER identity via healthIds (e.g. PMJAY, IRDAI, TPA-REG) and Participant.descriptor.name; payer type via payerArchetype in HealthConsideration
- Role-based conditional requirements: specialistAccreditation required for SPECIALIST
- PII handling: healthIds values, dateOfBirth, and gender are flagged as sensitive in profile.json
