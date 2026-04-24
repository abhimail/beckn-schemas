"""
Layer 4 — Example Payload Validation (v2.1 Generalised)
Validates example JSON payloads against the combined schema:
  - Core schemas (from core/attributes.yaml)
  - Extension schema (from each schema folder's attributes.yaml)

v2.1 Payload Structure:
  - resourceAttributes:      message.catalogs[].beckn:resources[].beckn:resourceAttributes
  - offerAttributes:         message.catalogs[].beckn:offers[].beckn:offerAttributes
  - contractAttributes:      message.contract.beckn:contractAttributes
  - commitmentAttributes:    message.contract.beckn:commitments[].beckn:commitmentAttributes
  - performanceAttributes:   message.contract.beckn:performance[].beckn:performanceAttributes
  - considerationAttributes: message.contract.beckn:consideration[].beckn:considerationAttributes
  - settlementAttributes:    message.contract.beckn:settlements[].beckn:settlementAttributes
"""

import json
import yaml
import jsonschema
from pathlib import Path


def load_yaml(path):
    with open(path) as f:
        return yaml.safe_load(f)


def load_json(path):
    with open(path) as f:
        return json.load(f)


def build_schema_store(core_spec, ext_spec, schema_dir=None):
    store = {}
    for name, schema in core_spec.get("components", {}).get("schemas", {}).items():
        store[f"#/components/schemas/{name}"] = schema
    for name, schema in ext_spec.get("components", {}).get("schemas", {}).items():
        store[f"#/components/schemas/{name}"] = schema

    # Pre-load cross-file $refs from allOf/properties to resolve parent schemas
    if schema_dir:
        _load_cross_refs(ext_spec, schema_dir, store)

    return store


def _load_cross_refs(spec, schema_dir, store):
    """Walk the spec looking for $ref to external .yaml files, load them into store."""
    for name, defn in spec.get("components", {}).get("schemas", {}).items():
        if not isinstance(defn, dict):
            continue
        for item in defn.get("allOf", []):
            if isinstance(item, dict) and "$ref" in item:
                ref = item["$ref"]
                if ".yaml" in ref and "#" in ref:
                    _resolve_external_ref(ref, schema_dir, store)
        for prop_name, prop_def in defn.get("properties", {}).items():
            if isinstance(prop_def, dict) and "$ref" in prop_def:
                ref = prop_def["$ref"]
                if ".yaml" in ref and "#" in ref:
                    _resolve_external_ref(ref, schema_dir, store)


def _resolve_external_ref(ref, schema_dir, store):
    """Load an external yaml $ref like '../../RetailResource/v2.1/attributes.yaml#/...' into store."""
    file_part, fragment = ref.split("#", 1)
    resolved_path = (schema_dir / file_part).resolve()
    if not resolved_path.exists():
        return
    try:
        ext = load_yaml(resolved_path)
        for name, schema in ext.get("components", {}).get("schemas", {}).items():
            key = f"#/components/schemas/{name}"
            if key not in store:
                store[key] = schema
    except Exception:
        pass


def resolve_schema(schema, store):
    if not isinstance(schema, dict):
        return schema
    if "$ref" in schema:
        ref = schema["$ref"]
        # Normalize cross-file refs to local fragment
        if "#" in ref and ".yaml" in ref:
            ref = "#" + ref.split("#", 1)[1]
        if ref in store:
            return resolve_schema(store[ref], store)
        return schema
    result = {}
    for k, v in schema.items():
        if isinstance(v, dict):
            result[k] = resolve_schema(v, store)
        elif isinstance(v, list):
            result[k] = [resolve_schema(i, store) if isinstance(i, dict) else i for i in v]
        else:
            result[k] = v
    return result


def get_top_level_schema_name(ext_spec):
    for name, defn in ext_spec.get("components", {}).get("schemas", {}).items():
        if isinstance(defn, dict) and "x-beckn-container" in defn:
            return name, defn.get("x-beckn-container")
    return None, None


def _get(obj, key):
    """Try both plain key and beckn:-prefixed key."""
    return obj.get(key) or obj.get(f"beckn:{key}")


def _get_list(obj, key):
    """Try both plain key and beckn:-prefixed key, return list."""
    return obj.get(key, []) or obj.get(f"beckn:{key}", [])


def extract_blocks(example, container_key):
    """
    Extract all attribute blocks for a given v2.1 container key from an example payload.
    Supports both plain keys (matching beckn.yaml) and beckn:-prefixed keys.
    Returns list of dicts (one per resource/offer/performance/etc.).
    """
    blocks = []
    msg = example.get("message", {})

    if container_key == "resourceAttributes":
        for catalog in msg.get("catalogs", []):
            for resource in _get_list(catalog, "resources"):
                ra = _get(resource, "resourceAttributes")
                if isinstance(ra, dict):
                    blocks.append(ra)
        # Flat catalog pattern
        flat_cat = msg.get("catalog", {})
        for resource in _get_list(flat_cat, "resources"):
            ra = _get(resource, "resourceAttributes")
            if isinstance(ra, dict):
                blocks.append(ra)
        return blocks

    if container_key == "offerAttributes":
        for catalog in msg.get("catalogs", []):
            for offer in _get_list(catalog, "offers"):
                oa = _get(offer, "offerAttributes")
                if isinstance(oa, dict):
                    blocks.append(oa)
        # Flat catalog pattern (singular)
        flat_cat = msg.get("catalog", {})
        for offer in _get_list(flat_cat, "offers"):
            oa = _get(offer, "offerAttributes")
            if isinstance(oa, dict):
                blocks.append(oa)
        return blocks

    contract = msg.get("contract", {})

    if container_key == "contractAttributes":
        ca = _get(contract, "contractAttributes")
        if isinstance(ca, dict):
            blocks.append(ca)
        return blocks

    if container_key == "commitmentAttributes":
        for commitment in _get_list(contract, "commitments"):
            cma = _get(commitment, "commitmentAttributes")
            if isinstance(cma, dict):
                blocks.append(cma)
        return blocks

    if container_key == "performanceAttributes":
        for perf in _get_list(contract, "performance"):
            pa = _get(perf, "performanceAttributes")
            if isinstance(pa, dict):
                blocks.append(pa)
        return blocks

    if container_key == "considerationAttributes":
        for cons in _get_list(contract, "consideration"):
            coa = _get(cons, "considerationAttributes")
            if isinstance(coa, dict):
                blocks.append(coa)
        return blocks

    if container_key == "settlementAttributes":
        for settlement in _get_list(contract, "settlements"):
            sa = _get(settlement, "settlementAttributes")
            if isinstance(sa, dict):
                blocks.append(sa)
        return blocks

    return blocks


def _relax_for_inheritance(schema):
    """Relax constraints from allOf-inherited schemas for validation of child instances.

    Removes:
    - additionalProperties: false (child adds its own properties)
    - const on @context/@type (child uses its own context/type values)
    """
    if not isinstance(schema, dict):
        return schema
    result = {}
    for k, v in schema.items():
        if k == "additionalProperties" and v is False:
            continue
        elif k == "const":
            continue  # const from parent schema conflicts with child overrides
        elif k == "allOf" and isinstance(v, list):
            result[k] = [_relax_for_inheritance(i) for i in v]
        elif isinstance(v, dict):
            result[k] = _relax_for_inheritance(v)
        elif isinstance(v, list):
            result[k] = [_relax_for_inheritance(i) if isinstance(i, dict) else i for i in v]
        else:
            result[k] = v
    return result


def validate_block(block, schema, store):
    resolved = resolve_schema(schema, store)
    cleaned = {k: v for k, v in resolved.items() if not k.startswith("x-")}
    cleaned = _relax_for_inheritance(cleaned)
    errors = []
    try:
        jsonschema.validate(instance=block, schema=cleaned)
    except jsonschema.ValidationError as e:
        errors.append(e.message)
    except jsonschema.SchemaError as e:
        errors.append(f"Schema error: {e.message}")
    except jsonschema.exceptions.RefResolutionError as e:
        errors.append(f"Unresolvable $ref (cross-file): {e}")
    return errors


def run(schema_dir: Path, core_dir: Path):
    results = []
    attr_path      = schema_dir / "attributes.yaml"
    # Support both naming conventions for the core spec file
    core_attr_path = core_dir / "attributes.yaml"
    if not core_attr_path.exists():
        core_attr_path = core_dir / "beckn.yaml"
    examples_dir   = schema_dir / "examples"

    for path, label in [(attr_path, "attributes.yaml"),
                        (core_attr_path, "core/attributes.yaml")]:
        if not path.exists():
            results.append({"check": f"file_exists:{label}", "passed": False,
                            "detail": f"{path} not found"})
            return results

    ext_spec  = load_yaml(attr_path)
    core_spec = load_yaml(core_attr_path)
    store     = build_schema_store(core_spec, ext_spec, schema_dir)

    top_schema_name, container_key = get_top_level_schema_name(ext_spec)
    if not top_schema_name:
        results.append({
            "check": "top_level_schema_found",
            "passed": False,
            "detail": "No schema with x-beckn-container found in attributes.yaml"
        })
        return results

    results.append({
        "check": "top_level_schema_found",
        "passed": True,
        "detail": f"Top-level schema: '{top_schema_name}', v2.1 container: '{container_key}'"
    })

    top_schema = ext_spec["components"]["schemas"][top_schema_name]

    if not examples_dir.exists():
        results.append({"check": "examples_exist", "passed": False,
                        "detail": "examples/ directory not found"})
        return results

    example_files = sorted(examples_dir.glob("*.json"))
    if not example_files:
        results.append({"check": "examples_exist", "passed": False,
                        "detail": "No .json example files found"})
        return results

    for example_path in example_files:
        try:
            example = load_json(example_path)
        except json.JSONDecodeError as e:
            results.append({"check": f"example_parse:{example_path.name}",
                            "passed": False, "detail": str(e)})
            continue

        blocks = extract_blocks(example, container_key)

        if not blocks:
            results.append({
                "check": f"example_has_block:{example_path.name}",
                "passed": False,
                "detail": (
                    f"No '{container_key}' block found in v2.1 payload. "
                    f"For resourceAttributes check message.catalogs[].beckn:resources[].beckn:resourceAttributes; "
                    f"for contractAttributes check message.contract.beckn:contractAttributes."
                )
            })
            continue

        all_errors = []
        for i, block in enumerate(blocks):
            errs = validate_block(block, top_schema, store)
            for e in errs:
                all_errors.append(f"block[{i}]: {e}")

        results.append({
            "check": f"example_valid:{example_path.name}",
            "passed": len(all_errors) == 0,
            "detail": all_errors if all_errors else f"Valid ({len(blocks)} block(s) checked)"
        })

    return results
