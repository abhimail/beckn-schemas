# CodedValue — Shared Type Definition

**Location:** `generic-service/generic-common/CodedValue/`
**Version:** 1.0.0
**Status:** Under review — upstream core candidacy pending

---

## What this is

`CodedValue` is a shared sub-schema for representing a single code drawn from an
external or administrative coding authority. It is **not** a first-class Beckn schema:
it has no `profile.json`, `context.jsonld`, or `renderer.json`, and carries no
`x-beckn-container` annotation. It exists only as a reusable type definition
referenced via `$ref` by schemas that need typed, machine-filterable coded values.

The pattern is modelled on [FHIR Coding](https://www.hl7.org/fhir/datatypes.html#Coding).

---

## The triple

```yaml
"@context": "https://lgdirectory.gov.in"   # authority URI
"@type":    "LGDDistrict"                   # code class within the authority
code:       "507"                           # the code string
display:    "Nashik"                        # optional human-readable label (informational)
```

The `(@context, @type, code)` triple uniquely identifies a value within the
authority's namespace. The `display` field is informational only — never filter on it.

---

## Why `generic-common/` and not a schema folder

`generic-common/` is the canonical location for shared type definitions that are
referenced across multiple schemas within the `generic-service` pack, or by
extension packs (`agri-services-ext`, domain-specific advisory packs, etc.).

A type definition lives in `generic-common/` rather than a full schema folder because:
- It has no independent lifecycle in the Beckn catalogue (no Resource, Offer, or Contract role).
- It has no network-participant-facing rendering.
- It is always embedded inside another schema's properties, never a top-level object.

Full schema folders carry seven artefacts (`attributes.yaml`, `profile.json`,
`context.jsonld`, `renderer.json`, `examples/`, `tests/`, `README.md`).
A shared type definition carries only `attributes.yaml` + `README.md`.

---

## Thumb rules

| Situation | Pattern |
|---|---|
| Code system maintained by an external authority (LGD, ISO, KNBS, WHO) | `CodedValue` |
| Small, stable value set owned by this schema | plain `enum` |
| Value is a free-text human label (county name, village name) | plain `string` |
| Value needs machine-filtering across implementations | `CodedValue` |

---

## Current consumers

| Schema | Field | Authority examples |
|---|---|---|
| `AgriServiceResource` (agri-services-ext) | `coverageAreaCodes` | LGD, KNBS, IEBC, India Post |
| `AgriCropAdvisoryResource` (agri-advisory-v21) | `cropTypes`, `coverageAreaCodes` (inherited) | FAO crop codes, LGD |
| `AgriWeatherResource` (agri-advisory-v21) | `weatherParameters`, `coverageAreaCodes` (inherited) | WMO, LGD |
| `AgriCommodityPriceResource` (agri-advisory-v21) | `commodities`, `marketCodes`, `coverageAreaCodes` (inherited) | FAO, APMC, LGD |
| `AgriDigitalPerformance` (agri-services-ext) | `targetLocation` | LGD, KNBS |

---

## Upstream candidacy

`CodedValue` is a strong candidate for promotion into the Beckn Protocol core
vocabulary (alongside `Credential`, `Location`, etc.). Until that promotion occurs,
`generic-service/generic-common/CodedValue/attributes.yaml` is the canonical
cross-pack reference point. Extension packs must `$ref` this file directly rather
than defining their own copy.

If your pack lives outside the `generic-service` folder tree, use the absolute
schema registry URI once registered:
```
$ref: "https://schema.beckn.io/generic-common/CodedValue/attributes.yaml#/components/schemas/CodedValue"
```
