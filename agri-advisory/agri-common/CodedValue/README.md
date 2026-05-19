# CodedValue — agri-advisory-v21 local re-export

This is a thin re-export of the canonical `CodedValue` shared type definition
which lives upstream at:

```
generic-service/generic-common/CodedValue/attributes.yaml
```

**Do not add schema content here.** All property definitions, documentation, and
thumb rules are maintained in the upstream file.

## Why this file exists

Schema `$ref` paths must be relative or use absolute registry URIs. Since
`agri-advisory-v21` lives in a different mounted folder from `generic-service`,
schemas in this pack reference this local re-export rather than constructing a
long cross-mount relative path on every usage.

Once `CodedValue` is promoted to the Beckn Protocol core vocabulary and published
at a stable registry URI, all references should be updated to the canonical URI:

```
$ref: "https://schema.beckn.io/generic-common/CodedValue/attributes.yaml#/components/schemas/CodedValue"
```
