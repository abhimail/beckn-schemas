# HealthParticipant — v2.1

**Schema Pack Version:** 2.1.0
**Released:** April 2026
**Network:** ONHS
**Status:** Initial release

### Container

- **Participant.participantAttributes**

### Key features

- Six participant roles: PATIENT, CARE_GIVER, SPECIALIST, FIELD_WORKER, PAYER, IMPLEMENTING_AGENCY
- ABHA (Ayushman Bharat Health Account) identifier support
- Specialist accreditation object (body, registration number, specialty, validity)
- Payer details (type, name, ID, scheme) for government and insurance payers
- Role-based conditional requirements: specialistAccreditation required for SPECIALIST; payerDetails required for PAYER
- PII handling: abhaId, dateOfBirth, gender are flagged as sensitive in profile.json
