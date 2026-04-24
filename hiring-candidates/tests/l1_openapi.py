"""
Layer 1 — OpenAPI 3.1.1 Structural Validation (v2.1 Generalised)
Validates each attributes.yaml without external packages.
Checks: required keys, schema types, $ref resolvability, x-jsonld-id presence,
        x-beckn-container presence with valid v2.1 container value.
"""

import yaml
from pathlib import Path


VALID_TYPES = {"string", "number", "integer", "boolean", "array", "object", "null"}

# Valid x-beckn-container values for v2.1 generalised schemas
VALID_V21_CONTAINERS = {
    "resourceAttributes",
    "offerAttributes",
    "contractAttributes",
    "commitmentAttributes",
    "performanceAttributes",
    "considerationAttributes",
    "settlementAttributes",
}

# Legacy v2 containers — flagged as wrong version if found
LEGACY_V2_CONTAINERS = {
    "itemAttributes",
    "fulfillmentAttributes",
    "orderAttributes",
}


def load_yaml(path):
    with open(path) as f:
        return yaml.safe_load(f)


def check_top_level(spec, path):
    issues = []
    for key in ("openapi", "info", "components"):
        if key not in spec:
            issues.append(f"Missing required top-level key: '{key}'")
    version = spec.get("openapi", "")
    if not str(version).startswith("3.1"):
        issues.append(f"Expected openapi: 3.1.x, got '{version}'")
    if "components" in spec and "schemas" not in spec["components"]:
        issues.append("components section has no 'schemas' key")
    return issues


def collect_internal_refs(obj):
    refs = set()
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "$ref" and isinstance(v, str) and v.startswith("#/"):
                refs.add(v)
            else:
                refs |= collect_internal_refs(v)
    elif isinstance(obj, list):
        for item in obj:
            refs |= collect_internal_refs(item)
    return refs


def resolve_ref(spec, ref):
    parts = ref.lstrip("#/").split("/")
    node = spec
    for part in parts:
        if not isinstance(node, dict) or part not in node:
            return False
        node = node[part]
    return True


def check_schemas(spec):
    issues = []
    schemas = spec.get("components", {}).get("schemas", {})
    if not schemas:
        issues.append("No schemas defined under components/schemas")
        return issues

    for schema_name, schema_def in schemas.items():
        if not isinstance(schema_def, dict):
            issues.append(f"Schema '{schema_name}' is not a mapping")
            continue

        stype = schema_def.get("type")
        if stype and stype not in VALID_TYPES:
            issues.append(f"Schema '{schema_name}': invalid type '{stype}'")

        for prop_name, prop_def in schema_def.get("properties", {}).items():
            if not isinstance(prop_def, dict):
                issues.append(f"'{schema_name}.{prop_name}': property definition is not a mapping")
                continue

            xjsonld = prop_def.get("x-jsonld-id")
            if xjsonld is None:
                issues.append(f"'{schema_name}.{prop_name}': missing x-jsonld-id annotation")
            elif not isinstance(xjsonld, str) or not xjsonld.strip():
                issues.append(f"'{schema_name}.{prop_name}': x-jsonld-id is empty or not a string")

            if prop_def.get("type") == "array" and "items" not in prop_def:
                issues.append(f"'{schema_name}.{prop_name}': array type missing 'items'")

    return issues


def check_refs(spec):
    issues = []
    refs = collect_internal_refs(spec)
    for ref in sorted(refs):
        if not resolve_ref(spec, ref):
            issues.append(f"Unresolvable $ref: '{ref}'")
    return issues


def check_x_beckn_container(spec):
    """
    Verify at least one schema declares x-beckn-container with a valid v2.1 value.
    Flag schemas that use legacy v2 container names.
    """
    issues = []
    schemas = spec.get("components", {}).get("schemas", {})

    declared = []
    for name, defn in schemas.items():
        if not isinstance(defn, dict):
            continue
        container = defn.get("x-beckn-container")
        if container is not None:
            declared.append((name, container))

    if not declared:
        issues.append(
            "No schema declares x-beckn-container — top-level schema must declare its "
            "v2.1 attachment point (e.g., x-beckn-container: resourceAttributes)"
        )
        return issues

    for schema_name, container in declared:
        if container in LEGACY_V2_CONTAINERS:
            issues.append(
                f"'{schema_name}' declares x-beckn-container: '{container}' — this is a "
                f"v2 legacy container. For v2.1 generalised schemas use one of: "
                f"{', '.join(sorted(VALID_V21_CONTAINERS))}"
            )
        elif container not in VALID_V21_CONTAINERS:
            issues.append(
                f"'{schema_name}' declares unknown x-beckn-container: '{container}'. "
                f"Valid v2.1 containers: {', '.join(sorted(VALID_V21_CONTAINERS))}"
            )

    return issues


def run(schema_dir: Path):
    yaml_path = schema_dir / "attributes.yaml"
    results = []

    if not yaml_path.exists():
        return [{"check": "file_exists", "passed": False, "detail": "attributes.yaml not found"}]

    try:
        spec = load_yaml(yaml_path)
    except yaml.YAMLError as e:
        return [{"check": "yaml_parse", "passed": False, "detail": str(e)}]

    checks = [
        ("top_level_structure", check_top_level(spec, yaml_path)),
        ("schema_definitions",  check_schemas(spec)),
        ("internal_refs",       check_refs(spec)),
        ("beckn_container_v21", check_x_beckn_container(spec)),
    ]

    for check_name, issues in checks:
        results.append({
            "check": check_name,
            "passed": len(issues) == 0,
            "detail": issues if issues else "OK",
        })

    return results
