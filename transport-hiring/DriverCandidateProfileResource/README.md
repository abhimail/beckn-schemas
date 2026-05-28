# DriverCandidateProfileResource Schema

**Container:** `Resource.resourceAttributes`
**Protocol Version:** 2.0
**Semantic Model:** generalised
**Use Cases:** UC2 — Operator Initiated Driver Recruitment
**Tag:** transport-hiring hiring resource

## Overview

DriverCandidateProfileResource captures the extension attributes for a driver candidate
profile published by a driver platform, aggregator, or self-enrolled driver. It extends
the generic `CandidateProfileResource` with fields specific to the transport vertical:
driver role types the candidate can perform, vehicle categories they are licensed for,
home location (at locality level for discovery), a reputation summary from the Driver
Passport network, and credential and training summaries.

All generic candidate fields (experience level, total experience years, availability
status, notice period, preferred work mode, skills, education, expected salary, languages,
open job types) are inherited from `CandidateProfileResource` and are not redefined here.

## Attachment Points

| Container | Schema | Reason |
|-----------|--------|--------|
| `beckn:resourceAttributes` | `DriverCandidateProfileResource` | Driver-specific candidate profile metadata extending the generic hiring resource |

The schema attaches only to `resourceAttributes`. Candidate PII (identity, precise
location, documents) is managed at the `beckn:parties` / credential level and does not
appear in this schema.

## Design Rationale

**Zero PII at discovery.** All fields in this schema are safe for publication in
`on_discover` responses. The one PII field (`passport_reference`) is stage-gated to
`init` and later via `x-pii-disclosure-stage`. Home location is disclosed at
locality level only — the `privacy_notes` in `profile.json` enforce this.

**`home_location` uses shared `JobLocation`.** The inline `NetworkLocation` sub-schema
from earlier drafts was replaced by a `$ref` to `hiring-common/JobLocation`, which
provides the same GPS + postal address combination with consistent field naming across
all hiring verticals.

**`credential_summary` and `training_summary` are label-only.** They carry credential
type enums and free-text training labels — no document references or verification
artefacts. Documents belong in the Driver Passport and are accessible post-init.

**`reputation_summary`** is inherited from `CandidateProfileResource` and provides a
network-wide trust signal from the Driver Passport system. It is not redefined here.

**Enum alignment with `DriverJobResource`.** The `driver_role_types` and
`vehicle_categories` enums in this schema are intentionally identical to the `role_type`
and `vehicle_categories_required` enums in `DriverJobResource`, enabling facet-match
filtering between job vacancies and candidate profiles at the Seeker NP.

## Non-Goals

- Does not model candidate identity or PII beyond the stage-gated `passport_reference`
- Does not model salary history or compensation expectations in detail (those belong in `offerAttributes`)
- Does not model application status or contract lifecycle (belongs in `contractAttributes`)
- Does not carry verification artefacts or credential documents (those are in Driver Passport)
- Does not model vehicle ownership — only licensing categories

## Upstream Candidates

The following properties may be generic enough for promotion to `CandidateProfileResource`:

- `credential_summary` (as a generic `credentialType[]` field for any regulated role)
- `training_summary` (as a generic `completedTraining[]` field)
- `passport_reference` (as a generic `networkIdentityRef` field with `x-pii-disclosure-stage`)
