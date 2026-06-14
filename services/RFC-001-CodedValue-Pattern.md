# RFC-001: CodedValue Pattern for Typed Codes in Beckn v2.1 Generalised Schema Extensions

**Status:** Draft — local working copy; not yet submitted to the Beckn repositories
**Author:** UAI Schema Working Group
**Created:** March 2026
**Applies to:** All Beckn v2.1 generalised schema packs; canonical type resides at `generic-service/generic-common/CodedValue/`

---

## 1. Problem Statement

Beckn v2.1 generalised extension schemas frequently need to reference codes from external or
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

## 2. Pattern: CodedValue

A `CodedValue` is a three-field object that makes the code system explicit,
following the same JSON-LD identity conventions already used throughout Beckn v2.1
generalised extension schemas (`@context`, `@type`).

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

*Examples from the agri-advisory domain: `deliveryMode`, `weatherOutputFormat`,
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

*Examples from the agri-advisory domain: `coverageAreaCodes` in `AgriServiceResource`
(administrative areas — LGD, PIN), `weatherParameters` in `AgriWeatherResource`
(meteorological parameters — WMO/CF alignment), `advisoryTypes` in
`AgriCropAdvisoryResource` (future alignment with FAO crop protection taxonomies).*

### Borderline cases:

| Field | Schema | Decision | Rationale |
|---|---|---|---|
| `forecastType` | `AgriWeatherResource` | Enum for now | UAI-owned, operationally closed, no current external alignment need |
| `forecastResolution` | `AgriWeatherResource` | Enum for now | Structural granularity descriptor, not a domain concept code |
| `weatherParameters` | `AgriWeatherResource` | **CodedValue[]** | WMO/CF alignment; resolved in v2.1 |
| `advisoryTypes` | `AgriCropAdvisoryResource` | **CodedValue[]** | FAO AGROVOC alignment; resolved in v2.1 |
| `coverageAreaCodes` | `AgriServiceResource` | **CodedValue[]** | External authority (LGD, PIN, others); multi-system by design |

---

## 4. CodedValue as a Canonical Shared Type

`CodedValue` is the canonical reusable sub-schema for typed codes across all
Beckn v2.1 generalised schema packs. It lives at:

```
generic-service/generic-common/CodedValue/attributes.yaml
$id: https://schema.beckn.io/CodedValue/v2.1/attributes.yaml
```

**Referencing CodedValue in your schema pack:**

- **Within the same pack** (e.g., another schema inside `generic-service`):
  use a relative path — `../../generic-common/CodedValue/v2.1/attributes.yaml`
- **From a different pack** (e.g., `agri-services-ext`, `agri-advisory-v21`):
  use the absolute schema.beckn.io URL —
  `https://schema.beckn.io/CodedValue/v2.1/attributes.yaml#/components/schemas/CodedValue`

The pattern is directly analogous to FHIR's `Coding` type — a well-established
precedent in health informatics DPI for exactly this problem. The key difference
is that `CodedValue` uses JSON-LD `@context` and `@type` conventions rather than
FHIR's `system`/`code`/`display` triplet, keeping it consistent with Beckn v2.1's
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

## 6. Adoption in Existing Schemas

This RFC does not require retrofitting all existing enum fields. Only fields
meeting the CodedValue criteria in §3 should be migrated. Fields already using
`CodedValue` in the agri-services-ext and agri-advisory-v21 packs:

- `AgriServiceResource.coverageAreaCodes` — administrative area codes (LGD, PIN);
  uses `CodedValue[]` from the start
- `AgriWeatherResource.weatherParameters` — meteorological parameter codes;
  uses `CodedValue[]` with WMO/CF alignment
- `AgriCropAdvisoryResource.advisoryTypes` — advisory type codes;
  uses `CodedValue[]` with FAO AGROVOC alignment path

---

## 7. Resolving a CodedValue to its Value Set (and Extending It)

*(Added June 2026.)* §2 defines the `CodedValue` shape and §3 when to use it. This section specifies, normatively, **how a consumer resolves a `CodedValue` to its valid `code` set**, and **how a network extends that set without forking a schema**.

### 7.1 Resolution rules

- **R1 — `@type` names the class.** It resolves, via the `@context` document, to a class IRI (e.g. `DeviationReasonCode` → `scoord:DeviationReasonCode`).
- **R2 — The value set is the co-located `vocab.jsonld`.** The authoritative members are the entries in the `vocab.jsonld` co-located with the `context.jsonld` named by `@context` (siblings in a pack `/<version>/` folder) whose `@type` is that class. `context.jsonld` carries term→IRI maps; `vocab.jsonld` carries the values.
- **R3 — `code` equals the member's `@id` local name** within that class (`"LAPSED"` ↔ `scoord:LAPSED`) — never the full IRI, never a disambiguating suffix (see §7.4).
- **R4 — Enforcement is layered.** OpenAPI checks `@type` (`const`) and that `@context` is a URI; JSON-LD expands `@type`/keys to IRIs; only a **vocab-aware validator / registry / network edge** checks `code` membership.
- **R5 — Admitting a code or code system is an edge rule**, not a schema constraint.

### 7.2 Self-owned vs. externally-governed

Self-owned values use a supporting class with **`const @type`** + an **open, defaulted `@context`** (default → the owning pack's `context.jsonld`); the value set is that pack's `vocab.jsonld`. Externally-governed values (LGD, PIN, ICD, SNOMED, …) use a **bare `CodedValue`** with open `@context`; membership is the receiver's responsibility. **Pin what you own; leave external authorities open.**

### 7.3 Extending a value set without forking

A network wanting its **own codes for an existing class** publishes only a **`context.jsonld` + `vocab.jsonld` pair** — declaring its prefix, aliasing the class name → `theirprefix:ClassName`, and declaring its members with `skos:exactMatch` to the base class's members where equivalents exist. It **reuses the schema structure unchanged** and emits its own `@context`. Registries store **native** codes; cross-network reconciliation is an **analytics-layer** task using the published `skos:exactMatch` maps. **Change the class → fork/extend the pack; change only the codes → publish a `context.jsonld` + `vocab.jsonld` pair.**

### 7.4 Member identity (no suffix leakage)

A value shared by two classes MUST be a **single node typed as both** — e.g. `{ "@id": "scoord:LAPSED", "@type": ["scoord:LifecycleState", "scoord:DeviationReasonCode"] }` — not two suffixed `@id`s. This preserves R3 (`code == @id` local name).

### 7.5 Anti-patterns

- Do **not** point `@context` at `vocab.jsonld` (it must be a JSON-LD context, not a value graph).
- Do **not** use the JSON-LD keyword `@vocab` as a node property (it is valid only inside a `@context`).
- Do **not** inline the value list as an OpenAPI `enum` on `code` unless you intend to **close** the set.
- Do **not** put a member `@id` / IRI on the wire as `code`; the wire value is the `@id` local name (R3).
