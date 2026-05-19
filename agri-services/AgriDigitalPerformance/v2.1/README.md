# AgriDigitalPerformance — v2.1

**Schema Pack Version:** 2.1.0
**Released:** May 2026
**Status:** Initial release

## Notes

Initial release of the AgriDigitalPerformance schema targeting the v2.1 generalised model.

This version introduces:
- `deliveryMode` enum covering APP, SMS, WHATSAPP, IVR, EMAIL, DASHBOARD, PUSH_NOTIFICATION, OTHER
- `requestedLanguage` and `deliveredLanguage` as BCP 47 language tags to track language fulfilment fidelity
- `contentAccessUrl` (URI) and `contentAccessExpiry` (date-time) for time-limited content links
- `targetLocation` as a `CodedValue` $ref for coded geographic scope of the advisory
- `contentRef` as an internal Provider NP content identifier for traceability
- `deliveredAt` timestamp for dispatch confirmation
- `deliveryConfirmed` boolean for end-to-end delivery confirmation

### Container

- **Performance.performanceAttributes**

### Key Features

- Explicit digital delivery channel tracking via `deliveryMode`
- Separate tracking of requested vs. delivered language for fulfilment auditing
- Time-limited content access URL support for pre-authenticated deep links
- Coded geographic scope via `targetLocation` (LGD, ISO 3166-2, GADM, etc.)
- End-to-end delivery confirmation flag compatible with SMS delivery reports and WhatsApp read receipts
- Extends all base ServicePerformance fields (appointment windows, completion flags, service notes, follow-up)

### Compatibility

- Requires Beckn Protocol core 2.0
- Depends on: `ServicePerformance` (allOf), `CodedValue` ($ref for targetLocation)
- Designed to be used alongside `AgriServiceResource` with `serviceCategory: DIGITAL_ADVISORY`
- No breaking changes expected for v2.2
