# RFC-001: CodedValue Pattern for Typed Codes in Beckn v2 Schema Extensions

**Status:** Draft
**Author:** UAI Schema Working Group
**Created:** March 2026
**Applies to:** All Beckn v2 extension schema packs

---

## 1. Problem Statement

Beckn v2 extension schemas frequently need to reference codes from external or
controlled vocabularies — administrative area codes (LGD, PIN), crop
classification systems (FAO AGROVOC), commodity codes, accreditation body
identifiers, and others. The current pattern is to use plain OpenAPI `enum`
arrays for all of these, which creates two problems:

1. **No type identity.** A bare string `"507"` carries no indication of which
   code system it belongs to. A consumer cannot distinguish an LGD district code
   from a PIN code or a commodity code without out-of-band knowledge.

2. **Conflates two distinct things.** Plain enums work well for closed, internally
   owned value sets. They are a poor fit for codes whose authority lives outside
   the schema pack — because enumerating them duplicates the authoritative source,
   goes stale, and creates a false impression that the schema owns the value set.

---

## 2. Proposed Pattern: CodedValue

A `CodedValue` is a three-field object that makes the code system explicit,
following the same JSON-LD identity conventions already used throughout Beckn v2
extension schemas (`@context`, `@type`).

```yaml
CodedValue:
  type: object
  required:
    - "@context"
    - "@type"
    - code
  additionalProperties: false
  properties:
    "@context":
      type: string
      format: uri
      description: >
        Canonical URI identifying the authoritative code system. For
        externally owned systems this is the authority's URI (e.g.
        https://lgdirectory.gov.in). For UAI-owned vocabularies this
        is the schema pack's context.jsonld path.
    "@type":
      type: string
      description: >
        Name of the code class within the identified context. For
        external systems this names the concept class (e.g. LGDDistrict).
        For UAI-owned vocabularies this is the enum type name defined
        in the relevant attributes.yaml (e.g. ForecastType).
    code:
      type: string
      description: >
        The code value. For externally owned systems, expected to be a
        valid member of the set defined by the authority at @context.
        For UAI-owned enums, must be one of the values defined under
        @type in the schema file. Schema validation enforces this for
        UAI-owned types; external code validation is the responsibility
        of the receiving participant.
```

### Example — external code (LGD district):
```json
{
  "@context": "https://lgdirectory.gov.in",
  "@type": "LGDDistrict",
  "code": "507"
}
```

### Example — UAI-owned enum (forecast resolution):
```json
{
  "@context": "./context.jsonld",
  "@type": "ForecastResolution",
  "code": "DISTRICT"
}
```

Both use identical structure. A consuming application processes them the same
way regardless of whether the authority is external or internal.

---

## 3. Thumb Rules: Local Enum vs CodedValue

Use these rules to decide which pattern to apply when designing a new field.

### Use a plain OpenAPI `enum` when:

- **You own the value set completely** and it will never need to reference or
  align with codes from any external system.
- **The values are operational/structural**, not domain concepts — e.g.
  `deliveryMode`, `outputFormat`, `lifecycleState`. These are implementation
  knobs internal to the network; external systems have no reason to reference
  them.
- **The set is small and stable** (typically ≤ 15 values) and unlikely to grow
  beyond what a developer can reason about at a glance.
- **Interoperability beyond the UAI network is not a goal** for this field.

*Examples from this schema pack: `deliveryMode`, `WeatherOutputFormat`,
`providerLicense`.*

### Use `CodedValue` when:

- **The authority for the value set is external** — a government body, standards
  organisation, or any system you do not control. You must not enumerate their
  codes in your schema.
- **The codes represent domain concepts** that other systems (APIs, datasets,
  partner networks) might want to align with or map to — e.g. crop types,
  weather parameters, administrative areas, commodity codes, disease taxonomies.
- **The same concept may need to be expressed using different coding systems**
  by different participants — e.g. a location that one BPP expresses as an LGD
  district code and another as a PIN code. `CodedValue` makes both forms
  structurally identical.
- **The field is a candidate for upstream promotion** to Beckn core or cross-domain
  reuse. `CodedValue` is the pattern that makes reuse possible without forcing
  all adopters to use the same code system.
- **You own the enum but it represents a named concept** that may evolve into
  interoperability with an external vocabulary over time (e.g. `forecastType`
  could eventually align with WMO product type codes).

*Examples from this schema pack: `coverageAreaCodes` (administrative areas),
`weatherDataPoints` (meteorological parameters — future alignment with WMO/CF
conventions), `advisoryCategory` (future alignment with FAO crop protection
taxonomies).*

### Borderline cases:

| Field | Decision | Rationale |
|---|---|---|
| `forecastType` | Enum for now | UAI-owned, operationally closed, no current external alignment need |
| `forecastResolution` | Enum for now | Structural granularity descriptor, not a domain concept code |
| `weatherDataPoints` | Enum now, CodedValue candidate | WMO/CF alignment possible; migrate when needed |
| `advisoryCategory` | Enum now, CodedValue candidate | FAO AGROVOC alignment possible; migrate when needed |
| `coverageAreaCodes` | **CodedValue** | External authority (LGD, PIN, others); multi-system by design |
| `targetLocation` area codes | **CodedValue** | Same as above |

---

## 4. CodedValue as an Upstream Candidate

`CodedValue` is proposed as a reusable sub-schema for promotion to Beckn core
(see §13.2 of the Implementation Guide). Any Beckn v2 domain that needs to
reference administrative areas, classification systems, or external vocabulary
codes will benefit from a consistent, JSON-LD-aligned structure for doing so.

The pattern is directly analogous to FHIR's `Coding` type — a well-established
precedent in health informatics DPI for exactly this problem. The key difference
is that `CodedValue` uses JSON-LD `@context` and `@type` conventions rather than
FHIR's `system`/`code`/`display` triplet, keeping it consistent with Beckn v2's
existing JSON-LD idiom.

---

## 5. Recommended UAI Code System Bindings

For implementations on the UAI network, the following `@context` + `@type`
combinations are recommended for common location reference needs:

| `@context` | `@type` | Scope | Example `code` |
|---|---|---|---|
| `https://lgdirectory.gov.in` | `LGDState` | Indian state | `"27"` (Maharashtra) |
| `https://lgdirectory.gov.in` | `LGDDistrict` | Indian district | `"507"` (Nashik) |
| `https://lgdirectory.gov.in` | `LGDSubDistrict` | Taluka / block | `"2342"` |
| `https://lgdirectory.gov.in` | `LGDVillage` | Village / revenue circle | `"583421"` |
| `https://www.indiapost.gov.in` | `PINCode` | India Post postal zone | `"422001"` |

These bindings are documented recommendations, not schema-enforced enums.
Validation of whether a given code exists in the authority's set is the
responsibility of the receiving BPP or BAP.

---

## 6. Impact on Existing Schemas

This RFC does not require retrofitting all existing enum fields. Only fields
meeting the CodedValue criteria in §3 should be migrated. The first fields
migrated in this schema pack are:

- `WeatherForecastItemAttributes.coverageAreaCodes` — new field, uses CodedValue from the start
- `AgriAdvisoryFulfillmentAttributes.targetLocation` — adds `areaCodes` array of CodedValue alongside existing GeoJSON field
