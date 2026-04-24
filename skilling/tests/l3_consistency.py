"""
Layer 3 — Cross-File Consistency (v2.1 Generalised)
Checks that context.jsonld, vocab.jsonld, and attributes.yaml are internally consistent.

Three checks per schema folder:
  A. Property coverage  — every property in attributes.yaml has a @id mapping in context.jsonld
  B. Prefix alignment   — x-jsonld-id values in attributes.yaml use the correct schema-specific
                          prefix (not a legacy flat prefix like 'drivernetwork:')
  C. Vocab coverage     — every enum class @id in vocab.jsonld that uses the schema prefix is
                          also declared as a type alias in context.jsonld
"""

import yaml
import json
from pathlib import Path


def load_yaml(path):
    with open(path) as f:
        return yaml.safe_load(f)


def load_json(path):
    with open(path) as f:
        return json.load(f)


def get_schema_properties(spec):
    result = {}
    for schema_name, schema_def in spec.get("components", {}).get("schemas", {}).items():
        if not isinstance(schema_def, dict):
            continue
        props = {}
        for prop_name, prop_def in schema_def.get("properties", {}).items():
            if isinstance(prop_def, dict):
                props[prop_name] = prop_def.get("x-jsonld-id")
        result[schema_name] = props
    return result


def get_context_mapped_terms(ctx_doc):
    ctx = ctx_doc.get("@context", {})
    mapped_terms = set()
    schema_prefix = None
    all_prefixes = {}

    for key, val in ctx.items():
        if key.startswith("@"):
            continue
        if isinstance(val, str):
            if val.endswith("#") and "schema.beckn.io" in val:
                schema_prefix = key
            if val.endswith("/") or val.endswith("#"):
                all_prefixes[key] = val
        elif isinstance(val, dict) and "@id" in val:
            mapped_terms.add(key)

    return mapped_terms, schema_prefix, all_prefixes


def get_vocab_classes(vocab_doc, schema_prefix):
    classes = set()
    prefix_str = f"{schema_prefix}:" if schema_prefix else None
    for entry in vocab_doc.get("@graph", []):
        entry_id = entry.get("@id", "")
        if prefix_str and entry_id.startswith(prefix_str):
            local = entry_id[len(prefix_str):]
            if entry.get("@type") == "rdfs:Class":
                classes.add(local)
    return classes


def check_property_coverage(schema_props, mapped_terms):
    issues = []
    for schema_name, props in schema_props.items():
        for prop_name in props:
            if prop_name.startswith("@"):
                continue  # JSON-LD keywords (@context, @type) are not domain properties
            if prop_name not in mapped_terms:
                issues.append(
                    f"'{schema_name}.{prop_name}' is in attributes.yaml "
                    f"but has no @id mapping in context.jsonld"
                )
    return issues


def check_prefix_alignment(schema_props, schema_prefix, all_prefixes):
    """
    x-jsonld-id values should use the correct schema-specific prefix.
    Flags use of known bad prefixes (legacy flat prefixes) or undeclared prefixes.
    """
    issues = []
    valid_prefixes = set(all_prefixes.keys()) | {"schema", "beckn", "xsd"}

    # Common legacy flat prefixes that indicate a migration issue
    KNOWN_LEGACY_PREFIXES = {
        "drivernetwork", "retailnetwork", "mobilitynetwork",
        "healthnetwork", "agrinetwork",
    }

    for schema_name, props in schema_props.items():
        for prop_name, x_jsonld_id in props.items():
            if not x_jsonld_id:
                continue
            if ":" not in x_jsonld_id:
                continue
            prefix_used = x_jsonld_id.split(":")[0]

            if prefix_used in KNOWN_LEGACY_PREFIXES:
                correct = (
                    f"{schema_prefix}:{x_jsonld_id.split(':', 1)[1]}"
                    if schema_prefix else "the schema-specific prefix"
                )
                issues.append(
                    f"'{schema_name}.{prop_name}': x-jsonld-id '{x_jsonld_id}' uses "
                    f"legacy flat prefix '{prefix_used}:' — should use '{correct}'"
                )
            elif prefix_used not in valid_prefixes:
                issues.append(
                    f"'{schema_name}.{prop_name}': x-jsonld-id '{x_jsonld_id}' uses "
                    f"undeclared prefix '{prefix_used}:'"
                )
    return issues


def check_vocab_coverage(vocab_classes, ctx_doc):
    issues = []
    ctx = ctx_doc.get("@context", {})
    ctx_class_aliases = set()
    for key, val in ctx.items():
        if isinstance(val, str) and ":" in val and not val.endswith("/") and not val.endswith("#"):
            ctx_class_aliases.add(key)

    for class_name in sorted(vocab_classes):
        if class_name not in ctx_class_aliases:
            issues.append(
                f"Vocab class '{class_name}' defined in vocab.jsonld "
                f"has no type alias in context.jsonld"
            )
    return issues


def run(schema_dir: Path):
    results = []

    attr_path    = schema_dir / "attributes.yaml"
    context_path = schema_dir / "context.jsonld"
    vocab_path   = schema_dir / "vocab.jsonld"

    for path, label in [(attr_path, "attributes.yaml"),
                        (context_path, "context.jsonld"),
                        (vocab_path, "vocab.jsonld")]:
        if not path.exists():
            results.append({"check": f"file_exists:{label}", "passed": False,
                            "detail": f"{label} not found"})
            return results

    spec      = load_yaml(attr_path)
    ctx_doc   = load_json(context_path)
    vocab_doc = load_json(vocab_path)

    schema_props                         = get_schema_properties(spec)
    mapped_terms, schema_prefix, all_pfx = get_context_mapped_terms(ctx_doc)
    vocab_classes                        = get_vocab_classes(vocab_doc, schema_prefix)

    issues_a = check_property_coverage(schema_props, mapped_terms)
    results.append({
        "check": "A_property_coverage",
        "passed": len(issues_a) == 0,
        "detail": issues_a if issues_a else f"All properties mapped ({len(mapped_terms)} terms)"
    })

    issues_b = check_prefix_alignment(schema_props, schema_prefix, all_pfx)
    results.append({
        "check": "B_prefix_alignment",
        "passed": len(issues_b) == 0,
        "detail": issues_b if issues_b else "All x-jsonld-id prefixes are correct"
    })

    issues_c = check_vocab_coverage(vocab_classes, ctx_doc)
    results.append({
        "check": "C_vocab_coverage",
        "passed": len(issues_c) == 0,
        "detail": issues_c if issues_c else f"All {len(vocab_classes)} vocab classes aliased in context"
    })

    return results
