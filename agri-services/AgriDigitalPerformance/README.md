# AgriDigitalPerformance Schema

**Container:** `Performance.performanceAttributes`
**Protocol Version:** 2.0
**Semantic Model:** generalised
**Use Cases:** Digital advisory delivery tracking, agri content access, SMS/WhatsApp advisory confirmation, IVR advisory records
**Tag:** service agri-services-ext performance digital

## Overview

AgriDigitalPerformance extends the generalised Beckn `ServicePerformance` schema with fields specific to the digital delivery of agricultural advisory content. Where `AgriServicePerformance` tracks physical on-farm service delivery (visits, vaccinations, screenings), `AgriDigitalPerformance` tracks how advisory content was dispatched and received through digital channels: SMS, WhatsApp, in-app push notification, IVR audio, email, or web dashboard.

This schema is the performanceAttributes counterpart to an `AgriServiceResource` whose `serviceCategory` is `DIGITAL_ADVISORY`. It allows Seeker NPs, network operators, and farmers to verify that an advisory was dispatched, in which language, to which geographic scope, and whether delivery was confirmed.

## Attachment Points

| Beckn Object | Field | Cardinality |
|---|---|---|
| `Performance` | `performanceAttributes` | 1..1 when schema active |
| `contract.performance[]` | `performanceAttributes` | 1..1 per performance record |

The schema attaches to each `Performance` object inside `contract.performance[]`. One contract may have multiple performance records — one per advisory dispatch event.

## Design Rationale

Digital agricultural advisory has characteristics not captured by generic `ServicePerformance`:

1. **Delivery channel diversity** — SMS, WhatsApp, IVR, app push, email and dashboard each have different confirmation mechanics, latency characteristics and regulatory considerations. The `deliveryMode` enum makes the channel explicit.
2. **Language tracking** — Farmers in India and East Africa may request advisories in their native language (Marathi, Swahili, Kannada) but receive them in a fallback language if the native-language content is unavailable. Both `requestedLanguage` and `deliveredLanguage` are captured separately.
3. **Content access** — Digital advisories often produce a URL or deep link through which the content can be re-accessed. `contentAccessUrl` and `contentAccessExpiry` support time-limited pre-authenticated links.
4. **Geographic scope confirmation** — Farmers and Seeker NPs need to verify the advisory was generated for the correct administrative area. `targetLocation` carries a coded geographic reference.
5. **Delivery confirmation** — SMS delivery reports, WhatsApp read receipts, and app open events allow the Provider NP to confirm the advisory reached the end recipient. `deliveryConfirmed` is a simple boolean flag.
6. **Content traceability** — `contentRef` links the performance record back to the specific content object in the Provider NP's content management system for grievance resolution and re-fetch.

These fields are entirely additive to `ServicePerformance` — no inherited field is overridden.

## Non-Goals

- This schema does not model the content of the advisory itself (the text, images, or audio of the advisory are external to the Beckn contract).
- It does not model financial settlement for the advisory delivery — that belongs in payment and settlement objects.
- It does not model the scheduling or appointment of advisory delivery — that is handled at the `resourceAttributes` level through `availabilitySchedule`.
- It does not apply to physical on-farm services — use `AgriServicePerformance` for vaccination visits, screenings, and in-person advisory.

## Upstream Candidates

The following fields are candidates for promotion to the base `ServicePerformance` schema if sufficient adoption is observed across non-agri digital service verticals:

| Field | Rationale for promotion |
|---|---|
| `deliveryMode` | Any digitally delivered service benefits from explicit channel tracking |
| `contentAccessUrl` / `contentAccessExpiry` | Document delivery, telemedicine, and e-learning use similar patterns |
| `deliveryConfirmed` | Generic confirmation flag useful for all async digital delivery |
| `requestedLanguage` / `deliveredLanguage` | Language tracking is relevant to any multi-lingual digital service |
