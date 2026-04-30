# HealthContract — v2.1

**Schema Pack Version:** 2.1.0
**Released:** April 2026
**Network:** ONHS (Open Network for Health Services)
**Status:** Initial release

## Notes

Contract-level attributes for a health service engagement. Carries the
`healthServiceType` discriminator that drives conditional mandatory field
rules across other Health* schemas at runtime.

### Container

- **Contract.contractAttributes**

### healthServiceType discriminator

The `healthServiceType` field is the central discriminator for the Health* schema pack.
Its value makes certain fields conditionally mandatory in sibling schemas:

| Value | Description | Key conditional fields |
|---|---|---|
| DIAGNOSTIC_ANALYTICS | AI-driven analysis | consentDocRef (required), clinicalInterpretation (HealthPerformance) |
| TELECONSULTATION | Remote practitioner consult | serviceLocation optional |
| PHYSICAL_CONSULTATION | In-person consult | serviceLocation required |
| RADIOLOGY | Imaging & report | artifactsGenerated required |
| LAB_TEST | Pathology test | artifactsGenerated required |

### Key features

- Health service type discriminator (5 types)
- Booking channel tracking (APP / VOICE / IN_PERSON / USSD / WHATSAPP / SMS)
- Field worker (FLW/facilitator) linkage
- Consent document reference linking to Descriptor.docs[]
- Camp ID linkage for UC2 multi-patient camp engagements
