"""
Layer 2 — JSON-LD Prefix Resolution (v2.1 Generalised)
Checks:
- No stale @import from removed core context URL (context.jsonld must be self-contained)
- Schema-specific prefix declared in context.jsonld
- Required prefixes self-declared (schema, beckn)
- All @id values in context.jsonld resolve via local prefixes
- No orphan properties in v2.1 attribute blocks in example payloads
"""

import json
import yaml
from pathlib import Path


SKIP_KEYS = {"@context", "@type", "@id", "@graph", "@import", "_comment",
             "_comment_flow", "_comment_bap", "_comment_bpp", "_comment_key_changes"}

# Required prefixes that every v2.1 context.jsonld must self-declare
REQUIRED_PREFIXES = {
    "schema": "https://schema.org/",
    "beckn": "https://schema.beckn.io/",
}

# Core Beckn v2.1 keys that are NOT domain extension properties
CORE_KEYS = {
    # Contract
    "beckn:id", "beckn:status", "beckn:parties", "beckn:commitments",
    "beckn:consideration", "beckn:performance", "beckn:settlements",
    "beckn:contractAttributes",
    # Participants (v2.1 replaces parties)
    "beckn:participants", "beckn:participantAttributes",
    # Resource
    "beckn:descriptor", "beckn:provider", "beckn:isAvailable", "beckn:availableTo",
    "beckn:resourceAttributes",
    # Offer
    "beckn:proposer", "beckn:resourceIds", "beckn:considerationIds",
    "beckn:resourceRefs", "beckn:addOnRefs",
    "beckn:proposedConsideration", "beckn:validity", "beckn:offerAttributes",
    # Performance
    "beckn:mode", "beckn:tracking", "beckn:support", "beckn:rating",
    "beckn:performanceAttributes",
    # Consideration
    "beckn:type", "beckn:amount", "beckn:considerationAttributes",
    # Settlement
    "beckn:settlementRef", "beckn:settlementAttributes",
    # Commitment
    "beckn:ref", "beckn:refType", "beckn:quantity", "beckn:commitmentAttributes",
    "beckn:resources", "beckn:offer", "beckn:commitmentIds", "beckn:considerationId",
    # Catalog
    "beckn:items", "beckn:offers", "beckn:isActive",
    "beckn:bppId", "beckn:bppUri",
    # Context fields
    "context", "message", "action", "version", "bap_id", "bap_uri",
    "bpp_id", "bpp_uri", "transaction_id", "message_id", "timestamp", "ttl",
    "schema_context", "schemaContext", "network_id",
    # Common sub-objects
    "id", "status", "state", "type", "name", "phone", "email",
    "value", "currency", "code",
    # Rating sub-fields
    "beckn:ratingValue", "beckn:ratingCount",
    # Legacy — tolerated in mixed payloads
    "beckn:participantId", "beckn:role",
}


def load_context(context_path):
    with open(context_path) as f:
        ctx_doc = json.load(f)
    raw_ctx = ctx_doc.get("@context", {})

    prefixes = {}
    term_map = {}
    schema_prefix = None
    import_uri = None

    # Check for @import at top level of the document (not inside @context)
    if "@import" in ctx_doc:
        import_uri = ctx_doc["@import"]

    for key, val in raw_ctx.items():
        if key == "@import":
            import_uri = val
            continue
        if key.startswith("@"):
            continue
        if isinstance(val, str):
            if val.endswith("/") or val.endswith("#"):
                prefixes[key] = val
                # Schema-specific prefix ends with '#' and points to schema.beckn.io
                # Use endswith("#") to distinguish from the beckn: prefix (ends with "/")
                if "schema.beckn.io" in val and val.endswith("#"):
                    schema_prefix = key
        elif isinstance(val, dict) and "@id" in val:
            term_map[key] = val["@id"]

    return prefixes, term_map, schema_prefix, import_uri


def resolve_id(term_id, prefixes):
    if term_id.startswith("http"):
        return term_id
    if ":" in term_id:
        prefix, local = term_id.split(":", 1)
        if prefix in prefixes:
            return prefixes[prefix] + local
    return None


def check_term_resolvable(term_id, prefixes):
    return resolve_id(term_id, prefixes) is not None


def get_primary_container(schema_dir):
    attr_path = schema_dir / "attributes.yaml"
    if not attr_path.exists():
        return None
    try:
        with open(attr_path) as f:
            spec = yaml.safe_load(f)
        for name, defn in spec.get("components", {}).get("schemas", {}).items():
            if isinstance(defn, dict) and "x-beckn-container" in defn:
                return defn["x-beckn-container"]
    except Exception:
        pass
    return None


def extract_attribute_blocks(example, primary_container=None):
    """
    Extract v2.1 attribute blocks from an example payload.
    Supports v2.1 payload structure:
      - resourceAttributes: message.catalogs[].beckn:resources[].beckn:resourceAttributes
      - offerAttributes:    message.catalogs[].beckn:offers[].beckn:offerAttributes
      - contractAttributes: message.contract.beckn:contractAttributes
      - performanceAttributes: message.contract.beckn:performance[].beckn:performanceAttributes
      - considerationAttributes: message.contract.beckn:consideration[].beckn:considerationAttributes
      - settlementAttributes: message.contract.beckn:settlements[].beckn:settlementAttributes
      - commitmentAttributes: message.contract.beckn:commitments[].beckn:commitmentAttributes
    """
    blocks = []
    msg = example.get("message", {})

    def want(key):
        return primary_container is None or key == primary_container

    # resourceAttributes — in catalogs[].beckn:resources[]
    if want("resourceAttributes"):
        for catalog in msg.get("catalogs", []):
            for resource in catalog.get("beckn:resources", []):
                ra = resource.get("beckn:resourceAttributes")
                if isinstance(ra, dict):
                    blocks.append(("resourceAttributes", ra))
        # Also check flat message.catalog.resources[] pattern
        catalog = msg.get("catalog", {})
        for resource in catalog.get("beckn:resources", []):
            ra = resource.get("beckn:resourceAttributes")
            if isinstance(ra, dict):
                blocks.append(("resourceAttributes", ra))

    # offerAttributes — in catalogs[].beckn:offers[]
    if want("offerAttributes"):
        for catalog in msg.get("catalogs", []):
            for offer in catalog.get("beckn:offers", []):
                oa = offer.get("beckn:offerAttributes")
                if isinstance(oa, dict):
                    blocks.append(("offerAttributes", oa))
        # Also check flat message.catalog.offers[] pattern
        flat_cat = msg.get("catalog", {})
        for offer in flat_cat.get("beckn:offers", []):
            oa = offer.get("beckn:offerAttributes")
            if isinstance(oa, dict):
                blocks.append(("offerAttributes", oa))

    contract = msg.get("contract", {})

    # contractAttributes — directly on contract
    if want("contractAttributes"):
        ca = contract.get("beckn:contractAttributes")
        if isinstance(ca, dict):
            blocks.append(("contractAttributes", ca))

    # commitmentAttributes — in contract.beckn:commitments[]
    if want("commitmentAttributes"):
        for commitment in contract.get("beckn:commitments", []):
            cma = commitment.get("beckn:commitmentAttributes")
            if isinstance(cma, dict):
                blocks.append(("commitmentAttributes", cma))

    # performanceAttributes — in contract.beckn:performance[]
    if want("performanceAttributes"):
        for perf in contract.get("beckn:performance", []):
            pa = perf.get("beckn:performanceAttributes")
            if isinstance(pa, dict):
                blocks.append(("performanceAttributes", pa))

    # considerationAttributes — in contract.beckn:consideration[]
    if want("considerationAttributes"):
        for cons in contract.get("beckn:consideration", []):
            coa = cons.get("beckn:considerationAttributes")
            if isinstance(coa, dict):
                blocks.append(("considerationAttributes", coa))

    # settlementAttributes — in contract.beckn:settlements[]
    if want("settlementAttributes"):
        for settlement in contract.get("beckn:settlements", []):
            sa = settlement.get("beckn:settlementAttributes")
            if isinstance(sa, dict):
                blocks.append(("settlementAttributes", sa))

    return blocks


def run(schema_dir: Path):
    context_path = schema_dir / "context.jsonld"
    examples_dir = schema_dir / "examples"
    results = []

    if not context_path.exists():
        return [{"check": "context_exists", "passed": False, "detail": "context.jsonld not found"}]

    prefixes, term_map, schema_prefix, import_uri = load_context(context_path)
    primary_container = get_primary_container(schema_dir)

    # Check: no stale @import (context.jsonld must be self-contained in v2.1)
    if import_uri is not None:
        results.append({
            "check": "no_stale_import",
            "passed": False,
            "detail": (
                f"Stale @import found: '{import_uri}' — remove it entirely. "
                f"v2.1 domain context.jsonld files are self-contained and must declare "
                f"all prefixes (schema, beckn, per-schema) directly."
            )
        })
    else:
        results.append({
            "check": "no_stale_import",
            "passed": True,
            "detail": "No stale @import — context.jsonld is self-contained"
        })

    # Check schema-specific prefix
    if not schema_prefix:
        results.append({
            "check": "schema_prefix_declared",
            "passed": False,
            "detail": "No schema-specific prefix found (expected 'abbr': 'https://schema.beckn.io/{SchemaName}#')"
        })
    else:
        results.append({
            "check": "schema_prefix_declared",
            "passed": True,
            "detail": f"Schema prefix: '{schema_prefix}:' → {prefixes.get(schema_prefix)}"
        })

    # Check required prefixes are self-declared with correct values
    prefix_issues = []
    for prefix_key, expected_val in REQUIRED_PREFIXES.items():
        actual_val = prefixes.get(prefix_key)
        if actual_val is None:
            prefix_issues.append(
                f"'{prefix_key}' prefix missing — must declare \"{prefix_key}\": \"{expected_val}\""
            )
        elif actual_val != expected_val:
            prefix_issues.append(
                f"'{prefix_key}' = '{actual_val}' — expected '{expected_val}'"
            )
    results.append({
        "check": "required_prefixes_declared",
        "passed": len(prefix_issues) == 0,
        "detail": prefix_issues if prefix_issues else "All required prefixes correctly declared"
    })

    # Check all @id values in term_map are resolvable
    unresolvable_ids = []
    for prop, term_id in term_map.items():
        if not check_term_resolvable(term_id, prefixes):
            unresolvable_ids.append(f"'{prop}' → '{term_id}' (prefix not declared in this context)")

    results.append({
        "check": "all_context_ids_resolvable",
        "passed": len(unresolvable_ids) == 0,
        "detail": unresolvable_ids if unresolvable_ids else f"All {len(term_map)} @id values resolve correctly"
    })

    # Check example payloads for orphan attribute properties
    if not examples_dir.exists():
        results.append({"check": "examples_exist", "passed": False, "detail": "examples/ directory not found"})
        return results

    example_files = list(examples_dir.glob("*.json"))
    if not example_files:
        results.append({"check": "examples_exist", "passed": False, "detail": "No example .json files found"})
        return results

    for example_path in sorted(example_files):
        orphan_props = []
        try:
            with open(example_path) as f:
                example = json.load(f)

            blocks = extract_attribute_blocks(example, primary_container)
            if not blocks:
                continue

            for block_key, block in blocks:
                for prop in block.keys():
                    if prop in SKIP_KEYS or prop in CORE_KEYS:
                        continue
                    if prop not in term_map:
                        orphan_props.append(f"'{prop}' (in {block_key}) has no mapping in context.jsonld")

        except (json.JSONDecodeError, Exception) as e:
            results.append({
                "check": f"example_parse:{example_path.name}",
                "passed": False,
                "detail": str(e)
            })
            continue

        results.append({
            "check": f"example_orphan_props:{example_path.name}",
            "passed": len(orphan_props) == 0,
            "detail": orphan_props if orphan_props else "All attribute properties mapped in context"
        })

    return results
