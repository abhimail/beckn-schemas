#!/usr/bin/env python3
"""
Verification Service Network — Postman Collection Generator v1.0

Generates:
  1. VS_Catalog_Publish_Collection.json
  2. VS_UC1_BusOperator_DL_Verification_Collection.json
  3. VS_UC2_EVFleet_DriverKYC_Collection.json
  4. VS_UC4_EVFleet_TechCert_Verification_Collection.json
  5. VS_Environment.json

Protocol: Beckn v2.0.0 + Verification Service schema pack v2.1.0
Cohort:   Shared Mobility (bus operators, EV fleet operators, EV tech)

Conventions:
  - version "2.0.0" const; schemaContext only on discover/on_discover
  - message.contract at select; offer.resourceIds in all BAP messages + on_status
  - contractAttributes absent at select/on_select; introduced by Requesting NP at init
  - Consideration: schema:PriceSpecification (no domain-specific schema in pack)
  - Subject in contractAttributes.subject — not a participant
  - Variable names: NP language (requesting_np_id, provider_np_id, etc.)
  - All descriptions/comments: "Requesting NP" / "Provider NP"
"""

import json, os

OUTPUT_DIR = "/sessions/festive-epic-wozniak/mnt/verification service/reference-flows"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── Context URLs ──────────────────────────────────────────────────────────────

RESOURCE_CTX = "https://schema.beckn.io/verification-service/VerificationResource/v2.1/context.jsonld"
OFFER_CTX    = "https://schema.beckn.io/verification-service/VerificationOffer/v2.1/context.jsonld"
CONTRACT_CTX = "https://schema.beckn.io/verification-service/VerificationContract/v2.1/context.jsonld"
PERF_CTX     = "https://schema.beckn.io/verification-service/VerificationPerformance/v2.1/context.jsonld"

SCHEMA_CTX_CATALOG = [RESOURCE_CTX, OFFER_CTX]

# ── Pre-generated message UUIDs ───────────────────────────────────────────────
# One stable UUID per request — fixed for reproducibility.

MSG_CAT = {
    "publish":    "a1b2c3d4-e5f6-4789-8b12-cd34ef567890",
    "on_publish": "b2c3d4e5-f6a7-4890-8c23-de45fa678901",
}

MSG_UC1 = {
    "discover":    "c3d4e5f6-a7b8-4012-8d34-ef5678901abc",
    "on_discover": "d4e5f6a7-b8c9-4123-8e45-fa6789012bcd",
    "select":      "e5f6a7b8-c9d0-4234-8f56-ab7890123cde",
    "on_select":   "f6a7b8c9-d0e1-4345-8a67-bc8901234def",
    "init":        "a7b8c9d0-e1f2-4456-8b78-cd9012345ef0",
    "on_init":     "b8c9d0e1-f2a3-4567-8c89-de0123456fa1",
    "confirm":     "c9d0e1f2-a3b4-4678-8d90-ef1234567ab2",
    "on_confirm":  "d0e1f2a3-b4c5-4789-8e01-fa2345678bc3",
    "status":      "e1f2a3b4-c5d6-4890-8f12-ab3456789cd4",
    "on_status":   "f2a3b4c5-d6e7-4901-8a23-bc4567890de5",
}

MSG_UC2 = {
    "discover":    "a3b4c5d6-e7f8-4012-8b34-cd5678901ef2",
    "on_discover": "b4c5d6e7-f8a9-4123-8c45-de6789012fa3",
    "select":      "c5d6e7f8-a9b0-4234-8d56-ef7890123ab4",
    "on_select":   "d6e7f8a9-b0c1-4345-8e67-fa8901234bc5",
    "init":        "e7f8a9b0-c1d2-4456-8f78-ab9012345cd6",
    "on_init":     "f8a9b0c1-d2e3-4567-8a89-bc0123456de7",
    "confirm":     "a9b0c1d2-e3f4-4678-8b90-cd1234567ef8",
    "on_confirm":  "b0c1d2e3-f4a5-4789-8c01-de2345678fa9",
    "status":      "c1d2e3f4-a5b6-4890-8d12-ef3456789ab0",
    "on_status":   "d2e3f4a5-b6c7-4901-8e23-fa4567890bc1",
}

MSG_UC4 = {
    "discover":    "e3f4a5b6-c7d8-4012-8f34-ab5678901cd2",
    "on_discover": "f4a5b6c7-d8e9-4123-8a45-bc6789012de3",
    "select":      "a5b6c7d8-e9f0-4234-8b56-cd7890123ef4",
    "on_select":   "b6c7d8e9-f0a1-4345-8c67-de8901234fa5",
    "init":        "c7d8e9f0-a1b2-4456-8d78-ef9012345ab6",
    "on_init":     "d8e9f0a1-b2c3-4567-8e89-fa0123456bc7",
    "confirm":     "e9f0a1b2-c3d4-4678-8f90-ab1234567cd8",
    "on_confirm":  "f0a1b2c3-d4e5-4789-8a01-bc2345678de9",
    "status":      "a1b2c3d4-e5f6-4890-8b12-cd3456789ef0",
    "on_status":   "b2c3d4e5-f6a7-4901-8c23-de4567890fa1",
}

# ── Helpers ───────────────────────────────────────────────────────────────────

HEADERS = [
    {"key": "Content-Type",  "value": "application/json"},
    {"key": "Authorization", "value": "Bearer {{auth_token}}",
     "description": "Network-issued JWT — set before running the collection."},
]

def ctx(action, msg_id, ts, include_bpp=True, schema_contexts=None):
    """Build Beckn v2.0.0 context. NP-language variable names; spec JSON keys unchanged."""
    c = {
        "domain":        "{{domain}}",
        "networkId":     "{{network_id}}",
        "action":        action,
        "version":       "2.0.0",
        "bapId":         "{{requesting_np_id}}",
        "bapUri":        "{{requesting_np_uri}}",
        "transactionId": "{{transaction_id}}",
        "messageId":     msg_id,
        "timestamp":     ts,
    }
    if include_bpp:
        c["bppId"]  = "{{provider_np_id}}"
        c["bppUri"] = "{{provider_np_uri}}"
    if schema_contexts is not None:
        c["schemaContext"] = schema_contexts
    return c

def req(name, url_raw, body, description=""):
    return {
        "name": name,
        "request": {
            "method": "POST",
            "header": HEADERS,
            "body": {
                "mode": "raw",
                "raw": json.dumps(body, indent=2, ensure_ascii=False),
                "options": {"raw": {"language": "json"}},
            },
            "url": {"raw": url_raw},
            "description": description,
        },
        "response": [],
    }

def folder(name, description, items):
    return {"name": name, "description": description, "item": items}

def col(name, description, variables, folders):
    return {
        "info": {
            "name": name,
            "description": description,
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
        },
        "variable": variables,
        "item": folders,
    }

def var(key, value, description=""):
    v = {"key": key, "value": value, "type": "string"}
    if description:
        v["description"] = description
    return v

# ── Shared catalog objects ────────────────────────────────────────────────────

RESOURCE_DL_FULL = {
    "id": "res-vs-dl-001",
    "descriptor": {
        "name": "Driving Licence Verification",
        "shortDesc": "Real-time DL verification against Parivahan Sewa (MoRTH)",
    },
    "resourceAttributes": {
        "@context": RESOURCE_CTX,
        "@type": "vr:VerificationResource",
        "verificationType": {"code": "DRIVING_LICENCE", "name": "Driving Licence Verification"},
        "supportedDocumentTypes": [{"code": "DRIVING_LICENCE", "name": "Motor Vehicle Driving Licence"}],
        "supportedJurisdictions": [{"code": "IN", "name": "India"}],
        "verificationMethod": "REAL_TIME_API",
        "requiredInputFields": [
            {"fieldName": "licenceNumber", "displayName": "Driving Licence Number",
             "fieldType": "STRING", "isRequired": True,
             "validationPattern": "^[A-Z]{2}[0-9]{2}[0-9]{4}[0-9]{7}$"},
            {"fieldName": "dateOfBirth", "displayName": "Date of Birth",
             "fieldType": "DATE", "isRequired": True},
            {"fieldName": "holderName", "displayName": "Holder Name (as on DL)",
             "fieldType": "STRING", "isRequired": True},
        ],
        "authoritativeSource": {
            "name": "Parivahan Sewa — Ministry of Road Transport and Highways",
            "url": "https://parivahan.gov.in",
            "type": "GOVERNMENT_DATABASE",
        },
        "outputFields": [
            {"fieldName": "holderName",       "displayName": "Holder Name",        "fieldType": "STRING"},
            {"fieldName": "licenceNumber",    "displayName": "Licence Number",     "fieldType": "STRING"},
            {"fieldName": "issueDate",        "displayName": "Issue Date",         "fieldType": "DATE"},
            {"fieldName": "expiryDate",       "displayName": "Expiry Date",        "fieldType": "DATE"},
            {"fieldName": "vehicleClasses",   "displayName": "Authorised Classes", "fieldType": "STRING"},
            {"fieldName": "issuingAuthority", "displayName": "Issuing RTO",        "fieldType": "STRING"},
        ],
        "complianceStandards": [
            {"code": "IT_ACT_2000",  "name": "Information Technology Act, 2000"},
            {"code": "DPDPA_2023",   "name": "Digital Personal Data Protection Act, 2023"},
        ],
    },
}
RESOURCE_DL_REF = {"id": "res-vs-dl-001"}

RESOURCE_IDENTITY_FULL = {
    "id": "res-vs-identity-001",
    "descriptor": {
        "name": "Identity Verification — Aadhaar eKYC",
        "shortDesc": "Real-time identity verification via UIDAI Aadhaar eKYC",
    },
    "resourceAttributes": {
        "@context": RESOURCE_CTX,
        "@type": "vr:VerificationResource",
        "verificationType": {"code": "IDENTITY", "name": "Identity Verification"},
        "supportedDocumentTypes": [
            {"code": "AADHAAR", "name": "Aadhaar Card"},
            {"code": "PAN",     "name": "Permanent Account Number Card"},
        ],
        "supportedJurisdictions": [{"code": "IN", "name": "India"}],
        "verificationMethod": "REAL_TIME_API",
        "requiredInputFields": [
            {"fieldName": "aadhaarNumber", "displayName": "Aadhaar Number",
             "fieldType": "STRING", "isRequired": True,
             "validationPattern": "^[2-9][0-9]{11}$"},
            {"fieldName": "consentOtp", "displayName": "OTP (sent to registered mobile)",
             "fieldType": "STRING", "isRequired": True},
        ],
        "authoritativeSource": {
            "name": "UIDAI — Unique Identification Authority of India",
            "url": "https://uidai.gov.in",
            "type": "GOVERNMENT_DATABASE",
        },
        "outputFields": [
            {"fieldName": "name",        "displayName": "Full Name",     "fieldType": "STRING"},
            {"fieldName": "dateOfBirth", "displayName": "Date of Birth", "fieldType": "DATE"},
            {"fieldName": "gender",      "displayName": "Gender",        "fieldType": "STRING"},
            {"fieldName": "address",     "displayName": "Address",       "fieldType": "OBJECT"},
            {"fieldName": "photo",       "displayName": "Photo",         "fieldType": "IMAGE"},
        ],
        "complianceStandards": [
            {"code": "UIDAI_AUA",  "name": "UIDAI AUA/KUA Regulations"},
            {"code": "DPDPA_2023", "name": "Digital Personal Data Protection Act, 2023"},
        ],
    },
}
RESOURCE_IDENTITY_REF = {"id": "res-vs-identity-001"}

RESOURCE_SKILL_FULL = {
    "id": "res-vs-skill-001",
    "descriptor": {
        "name": "Skill Certificate Verification",
        "shortDesc": "Hybrid verification of NSDC and Sector Skill Council certificates",
    },
    "resourceAttributes": {
        "@context": RESOURCE_CTX,
        "@type": "vr:VerificationResource",
        "verificationType": {"code": "SKILL_CERTIFICATE", "name": "Skill Certificate Verification"},
        "supportedDocumentTypes": [
            {"code": "SKILL_CERT",  "name": "NSDC / Sector Skill Council Certificate"},
            {"code": "DEGREE_CERT", "name": "Vocational Training Degree Certificate"},
        ],
        "supportedJurisdictions": [{"code": "IN", "name": "India"}],
        "verificationMethod": "HYBRID",
        "requiredInputFields": [
            {"fieldName": "certificateNumber", "displayName": "Certificate Number",
             "fieldType": "STRING", "isRequired": True},
            {"fieldName": "holderName", "displayName": "Certificate Holder Name",
             "fieldType": "STRING", "isRequired": True},
            {"fieldName": "issuingBody", "displayName": "Issuing Body / Sector Skill Council",
             "fieldType": "STRING", "isRequired": True},
            {"fieldName": "issueYear", "displayName": "Year of Issue",
             "fieldType": "NUMBER", "isRequired": False},
        ],
        "authoritativeSource": {
            "name": "Skill India Portal — National Skill Development Corporation",
            "url": "https://www.skillindia.gov.in",
            "type": "GOVERNMENT_DATABASE",
        },
        "outputFields": [
            {"fieldName": "holderName",        "displayName": "Holder Name",           "fieldType": "STRING"},
            {"fieldName": "certificateNumber", "displayName": "Certificate Number",    "fieldType": "STRING"},
            {"fieldName": "skillName",         "displayName": "Skill / Trade Name",    "fieldType": "STRING"},
            {"fieldName": "qualificationPack", "displayName": "Qualification Pack ID", "fieldType": "STRING"},
            {"fieldName": "issuingBody",       "displayName": "Issuing Body",          "fieldType": "STRING"},
            {"fieldName": "issueDate",         "displayName": "Issue Date",            "fieldType": "DATE"},
            {"fieldName": "expiryDate",        "displayName": "Expiry Date",           "fieldType": "DATE"},
        ],
        "complianceStandards": [
            {"code": "NSQF",       "name": "National Skills Qualifications Framework"},
            {"code": "DPDPA_2023", "name": "Digital Personal Data Protection Act, 2023"},
        ],
    },
}
RESOURCE_SKILL_REF = {"id": "res-vs-skill-001"}

# ── Offers ────────────────────────────────────────────────────────────────────

OFFER_DL_FULL = {
    "id": "offer-vs-dl-std-001",
    "resourceIds": ["res-vs-dl-001"],
    "descriptor": {
        "name": "DL Verification — Standard",
        "shortDesc": "Real-time DL verification, result within 30 minutes",
    },
    "offerAttributes": {
        "@context": OFFER_CTX,
        "@type": "vo:VerificationOffer",
        "turnaroundTime":        "PT30M",
        "resultValidityPeriod":  "P90D",
        "pricingModel":          "PER_REQUEST",
        "serviceLevel":          "STANDARD",
        "dataRetentionPolicy":   "P30D",
        "supportedConsentMechanisms": ["OTP", "DIGITAL_SIGNATURE"],
    },
    "considerations": [{
        "id": "cons-vs-dl-cat-001",
        "considerationAttributes": {
            "@type": "schema:PriceSpecification",
            "price": 250, "priceCurrency": "INR",
            "valueAddedTaxIncluded": False,
            "description": "Per-request DL verification fee, excluding GST",
        },
    }],
}
OFFER_DL_REF = {"id": "offer-vs-dl-std-001", "resourceIds": ["res-vs-dl-001"]}

OFFER_IDENTITY_FULL = {
    "id": "offer-vs-identity-instant-001",
    "resourceIds": ["res-vs-identity-001"],
    "descriptor": {
        "name": "Identity Verification — Instant KYC",
        "shortDesc": "Aadhaar eKYC with verified result in under 5 minutes",
    },
    "offerAttributes": {
        "@context": OFFER_CTX,
        "@type": "vo:VerificationOffer",
        "turnaroundTime":        "PT5M",
        "resultValidityPeriod":  "P1Y",
        "pricingModel":          "PER_REQUEST",
        "serviceLevel":          "PREMIUM",
        "dataRetentionPolicy":   "P7D",
        "supportedConsentMechanisms": ["AADHAAR_EKYC", "OTP"],
    },
    "considerations": [{
        "id": "cons-vs-identity-cat-001",
        "considerationAttributes": {
            "@type": "schema:PriceSpecification",
            "price": 150, "priceCurrency": "INR",
            "valueAddedTaxIncluded": False,
            "description": "Per-request Aadhaar eKYC fee, excluding GST",
        },
    }],
}
OFFER_IDENTITY_REF = {"id": "offer-vs-identity-instant-001", "resourceIds": ["res-vs-identity-001"]}

OFFER_SKILL_FULL = {
    "id": "offer-vs-skill-hybrid-001",
    "resourceIds": ["res-vs-skill-001"],
    "descriptor": {
        "name": "Skill Certificate Verification — Hybrid",
        "shortDesc": "NSDC skill certificate verification, result within 1 business day",
    },
    "offerAttributes": {
        "@context": OFFER_CTX,
        "@type": "vo:VerificationOffer",
        "turnaroundTime":        "P1D",
        "resultValidityPeriod":  "P6M",
        "pricingModel":          "PER_REQUEST",
        "serviceLevel":          "STANDARD",
        "dataRetentionPolicy":   "P30D",
        "supportedConsentMechanisms": ["OTP", "DIGITAL_SIGNATURE", "OFFLINE_CONSENT"],
    },
    "considerations": [{
        "id": "cons-vs-skill-cat-001",
        "considerationAttributes": {
            "@type": "schema:PriceSpecification",
            "price": 350, "priceCurrency": "INR",
            "valueAddedTaxIncluded": False,
            "description": "Per-request skill certificate verification fee, excluding GST",
        },
    }],
}
OFFER_SKILL_REF = {"id": "offer-vs-skill-hybrid-001", "resourceIds": ["res-vs-skill-001"]}

# ── Full catalog (used in on_discover and catalog/publish) ────────────────────

CATALOG_FULL = {
    "id": "cat-vs-trustverify-001",
    "descriptor": {
        "name": "TrustVerify India — Verification Service Catalog",
        "shortDesc": "DL, identity, and skill certificate verification for the shared mobility sector",
    },
    "provider": {
        "id": "{{provider_np_id}}",
        "descriptor": {
            "name":      "TrustVerify India Pvt. Ltd.",
            "shortDesc": "CERT-In empanelled verification service provider; authorised UIDAI AUA",
        },
    },
    "resources": [RESOURCE_DL_FULL, RESOURCE_IDENTITY_FULL, RESOURCE_SKILL_FULL],
    "offers":    [OFFER_DL_FULL, OFFER_IDENTITY_FULL, OFFER_SKILL_FULL],
}


# =============================================================================
# COLLECTION 1 — CATALOG PUBLISH
# =============================================================================

def build_catalog_publish():
    desc = """\
## Verification Service Network — Catalog Publish

**Scenario:** TrustVerify India (Provider NP) publishes its verification service
catalog to the network registry / CDS, advertising three verification resources:
driving licence, identity (Aadhaar eKYC), and skill certificate verification.

**Protocol:** Beckn v2.0.0 + Verification Service schema pack v2.1.0

### Resources published

| Resource ID | Verification Type | Method | Turnaround |
|---|---|---|---|
| res-vs-dl-001 | DRIVING_LICENCE | REAL_TIME_API | PT30M |
| res-vs-identity-001 | IDENTITY (Aadhaar eKYC) | REAL_TIME_API | PT5M |
| res-vs-skill-001 | SKILL_CERTIFICATE | HYBRID | P1D |

### Pricing

| Offer ID | Rate | Model |
|---|---|---|
| offer-vs-dl-std-001 | ₹250/request | PER_REQUEST |
| offer-vs-identity-instant-001 | ₹150/request | PER_REQUEST |
| offer-vs-skill-hybrid-001 | ₹350/request | PER_REQUEST |

No status field on catalog considerations — status is a transaction-flow concept.

### Quick-start: environment setup

1. Import **VS_Environment.json** into Postman (Environments → Import).
2. Select the **Verification Service Network** environment.
3. Set `base_url` / `provider_np_uri` and `auth_token` for your target environment.
4. `network_id` is a placeholder — confirm the exact value with the network registry team.
"""

    publish_body = {
        "context": {
            "domain":    "{{domain}}",
            "networkId": "{{network_id}}",
            "action":    "catalog/publish",
            "version":   "2.0.0",
            "bppId":     "{{provider_np_id}}",
            "bppUri":    "{{provider_np_uri}}",
            "messageId": MSG_CAT["publish"],
            "timestamp": "2026-05-01T08:00:00+05:30",
        },
        "message": {"catalog": CATALOG_FULL},
    }

    on_publish_body = {
        "context": {
            "domain":    "{{domain}}",
            "networkId": "{{network_id}}",
            "action":    "catalog/on_publish",
            "version":   "2.0.0",
            "bppId":     "{{provider_np_id}}",
            "bppUri":    "{{provider_np_uri}}",
            "messageId": MSG_CAT["on_publish"],
            "timestamp": "2026-05-01T08:00:05+05:30",
        },
        "message": {
            "ack": {"status": "ACK"},
            "catalogId": "cat-vs-trustverify-001",
        },
    }

    variables = [
        var("registry_url",    "",               "Network registry / CDS endpoint — set per environment"),
        var("provider_np_uri", "",               "Provider NP (BPP) callback URI"),
        var("provider_np_id",  "trustverify.in", "Provider NP network identifier"),
        var("domain",          "vs:verification","Confirm exact domain prefix with network team"),
        var("network_id",      "vs.in/verification", "Confirm exact value with network registry team"),
        var("auth_token",      "",               "Network-issued JWT — set before running"),
    ]

    folders = [
        folder("01 — catalog/publish",
               "Provider NP sends its full catalog (3 verification resources + offers) to the network registry / CDS.",
               [req("catalog/publish", "{{registry_url}}/catalog/publish", publish_body,
                    "**catalog/publish** — Provider NP → Registry/CDS\n\n"
                    "TrustVerify India publishes its verification service catalog advertising "
                    "DL, identity, and skill certificate verification services.")]),
        folder("02 — catalog/on_publish",
               "Registry / CDS acknowledges successful catalog ingestion.",
               [req("catalog/on_publish", "{{provider_np_uri}}/catalog/on_publish", on_publish_body,
                    "**catalog/on_publish** — Registry/CDS → Provider NP\n\n"
                    "Registry acknowledges that the catalog has been successfully ingested and indexed.")]),
    ]

    return col("VS — Catalog Publish", desc, variables, folders)


# =============================================================================
# COLLECTION 2 — UC1: BUS OPERATOR DL VERIFICATION
# =============================================================================

def build_uc1():
    desc = """\
## Verification Service Network — UC1: Bus Operator Driving Licence Verification

**Scenario:** CityExpress Bus Services (Requesting NP) verifies the heavy motor
vehicle driving licence of driver applicant Ravi Kumar via TrustVerify India
(Provider NP) during employment onboarding. Real-time lookup against Parivahan
Sewa; result available within 30 minutes. On confirmation the contract is active
and verification is in progress (PENDING). On status poll, the result is returned
as VERIFIED with a signed PDF certificate.

**Protocol:** Beckn v2.0.0 + Verification Service schema pack v2.1.0
**Verification type:** DRIVING_LICENCE | **Method:** REAL_TIME_API | **Turnaround:** PT30M
**Purpose:** EMPLOYMENT_ONBOARDING | **Consent:** OTP

### Structural conventions

- `select` carries a DRAFT `Contract` (per `SelectAction.contract` in core spec)
- BAP originates the contract without an id; Provider NP assigns id at `on_select`
- `contractAttributes` absent at select / on_select — subject not yet identified
- BAP introduces subject, purpose, and consent reference at `init`
- `on_confirm` returns aggregateResult PENDING — verification is async (PT30M SLA)
- `on_status` returns aggregateResult VERIFIED + performance record + issuedCredentials

### Consideration lifecycle

| Call | status.code | price | notes |
|---|---|---|---|
| catalog (on_discover) | *(none)* | ₹250 | no status on catalog |
| on_select | PENDING | ₹250 | priced; Requesting NP has not yet committed |
| init | PENDING | ₹250 | Requesting NP echoes binding intent |
| on_init | QUOTED | ₹250 | binding quote; payment instructions out-of-band |
| confirm / on_confirm / on_status | ACTIVE | ₹250 | payment authorisation submitted |

### Quick-start: environment setup

1. Import **VS_Environment.json** (Environments → Import) and select it.
2. Set `base_url`, `requesting_np_uri`, `provider_np_uri`, and `auth_token`.
3. Run folders 01–10 in order.
"""

    # ── Shared objects ────────────────────────────────────────────────────────

    COMMITMENT_UC1_DRAFT_REF = {
        "id": "commitment-uc1-dl-001",
        "status": {"descriptor": {"code": "DRAFT"}},
        "resources": [dict(RESOURCE_DL_REF, **{"quantity": {"count": 1}})],
        "offer": OFFER_DL_REF,
    }

    COMMITMENT_UC1_DRAFT_FULL = {
        "id": "commitment-uc1-dl-001",
        "status": {"descriptor": {"code": "DRAFT"}},
        "resources": [dict(RESOURCE_DL_FULL, **{"quantity": {"count": 1}})],
        "offer": OFFER_DL_FULL,
    }

    COMMITMENT_UC1_ACTIVE_REF = {
        "id": "commitment-uc1-dl-001",
        "status": {"descriptor": {"code": "ACTIVE"}},
        "resources": [dict(RESOURCE_DL_REF, **{"quantity": {"count": 1}})],
        "offer": OFFER_DL_REF,
    }

    COMMITMENT_UC1_ACTIVE_FULL = {
        "id": "commitment-uc1-dl-001",
        "status": {"descriptor": {"code": "ACTIVE"}},
        "resources": [dict(RESOURCE_DL_FULL, **{"quantity": {"count": 1}})],
        "offer": OFFER_DL_FULL,
    }

    PARTICIPANT_UC1_MINIMAL = {"id": "part-uc1-cityexpress-001"}

    PARTICIPANT_UC1_FULL = {
        "id": "part-uc1-cityexpress-001",
        "role": "REQUESTER",
        "descriptor": {
            "name":      "CityExpress Bus Services Pvt. Ltd.",
            "shortDesc": "Requesting NP — intercity bus operator, Karnataka",
        },
    }

    def cons_uc1(status_code, extra=None):
        attrs = {
            "@type": "schema:PriceSpecification",
            "price": 250, "priceCurrency": "INR",
            "valueAddedTaxIncluded": False,
            "description": "Per-request DL verification fee, excluding GST",
        }
        if extra:
            attrs.update(extra)
        c = {
            "id": "cons-vs-dl-cat-001",
            "status": {"code": status_code},
            "considerationAttributes": attrs,
        }
        return c

    CONTRACT_ATTRS_UC1_INIT = {
        "@context": CONTRACT_CTX,
        "@type": "vc:VerificationContract",
        "subject": {
            "name": "Ravi Kumar",
            "dateOfBirth": "1992-03-15",
            "identifiers": [
                {"type": "LICENCE_NUMBER", "value": "KA0120190123456",
                 "maskedValue": "KA01XXXX123456"},
                {"type": "MOBILE", "value": "{{subject_mobile_masked}}",
                 "maskedValue": "XXXXXXX4521"},
            ],
        },
        "purpose": {
            "code": "EMPLOYMENT_ONBOARDING",
            "description": "Verification of driving licence for HMV driver employment onboarding",
        },
        "consentReference": {
            "consentId": "consent-uc1-rk-001",
            "mechanism": "OTP",
            "grantedAt": "2026-05-12T10:28:00+05:30",
            "expiresAt": "2026-05-12T11:28:00+05:30",
            "scope": ["DRIVING_LICENCE"],
        },
        "requestedBy": {
            "organizationName": "CityExpress Bus Services Pvt. Ltd.",
            "organizationType": "EMPLOYER",
            "referenceId": "onboarding-case-ce-2026-0512-001",
        },
    }

    # ── Payloads ──────────────────────────────────────────────────────────────

    discover_body = {
        "context": ctx("discover", MSG_UC1["discover"], "2026-05-12T10:15:00+05:30",
                       include_bpp=False, schema_contexts=SCHEMA_CTX_CATALOG),
        "message": {
            "intent": {
                "filters": "$.catalogs[*].resources[*] ? (@.resourceAttributes.verificationType.code == \"DRIVING_LICENCE\")",
            },
        },
    }

    on_discover_body = {
        "context": ctx("on_discover", MSG_UC1["on_discover"], "2026-05-12T10:15:03+05:30",
                       schema_contexts=SCHEMA_CTX_CATALOG),
        "message": {"catalogs": [CATALOG_FULL]},
    }

    select_body = {
        "context": ctx("select", MSG_UC1["select"], "2026-05-12T10:28:00+05:30"),
        "message": {
            "contract": {
                "status": {"code": "DRAFT"},
                "commitments": [COMMITMENT_UC1_DRAFT_REF],
                "participants": [PARTICIPANT_UC1_MINIMAL],
            },
        },
    }

    on_select_body = {
        "context": ctx("on_select", MSG_UC1["on_select"], "2026-05-12T10:28:02+05:30"),
        "message": {
            "contract": {
                "id": "{{contract_id}}",
                "status": {"code": "DRAFT"},
                "commitments": [COMMITMENT_UC1_DRAFT_FULL],
                "consideration": [cons_uc1("PENDING")],
                "participants": [PARTICIPANT_UC1_MINIMAL],
            },
        },
    }

    init_body = {
        "context": ctx("init", MSG_UC1["init"], "2026-05-12T10:29:00+05:30"),
        "message": {
            "contract": {
                "id": "{{contract_id}}",
                "status": {"code": "DRAFT"},
                "commitments": [COMMITMENT_UC1_DRAFT_REF],
                "consideration": [cons_uc1("PENDING")],
                "participants": [PARTICIPANT_UC1_FULL],
                "contractAttributes": CONTRACT_ATTRS_UC1_INIT,
            },
        },
    }

    on_init_body = {
        "context": ctx("on_init", MSG_UC1["on_init"], "2026-05-12T10:29:02+05:30"),
        "message": {
            "contract": {
                "id": "{{contract_id}}",
                "status": {"code": "DRAFT"},
                "commitments": [COMMITMENT_UC1_DRAFT_FULL],
                "consideration": [cons_uc1("QUOTED", {
                    "selectedPaymentMethod": "UPI",
                    "paymentSchedule": "UPFRONT",
                })],
                "participants": [PARTICIPANT_UC1_FULL],
                "contractAttributes": CONTRACT_ATTRS_UC1_INIT,
            },
        },
    }

    confirm_body = {
        "context": ctx("confirm", MSG_UC1["confirm"], "2026-05-12T10:30:00+05:30"),
        "message": {
            "contract": {
                "id": "{{contract_id}}",
                "status": {"code": "ACTIVE"},
                "commitments": [COMMITMENT_UC1_ACTIVE_REF],
                "consideration": [cons_uc1("ACTIVE", {
                    "selectedPaymentMethod": "UPI",
                    "transactionRef": "{{payment_ref}}",
                    "paymentAuthorisation": {
                        "authCode": "{{payment_ref}}",
                        "authProvider": "HDFC_UPI",
                        "authTimestamp": "2026-05-12T10:29:55+05:30",
                        "authAmount": 250,
                    },
                })],
                "participants": [PARTICIPANT_UC1_FULL],
                "contractAttributes": CONTRACT_ATTRS_UC1_INIT,
            },
        },
    }

    on_confirm_body = {
        "context": ctx("on_confirm", MSG_UC1["on_confirm"], "2026-05-12T10:30:05+05:30"),
        "message": {
            "contract": {
                "id": "{{contract_id}}",
                "status": {"code": "ACTIVE"},
                "descriptor": {
                    "name": "DL Verification — CityExpress / Ravi Kumar",
                    "shortDesc": "Verification in progress — result expected by 11:00 IST",
                },
                "commitments": [COMMITMENT_UC1_ACTIVE_FULL],
                "consideration": [cons_uc1("ACTIVE", {
                    "selectedPaymentMethod": "UPI",
                    "transactionRef": "{{payment_ref}}",
                })],
                "participants": [PARTICIPANT_UC1_FULL],
                "contractAttributes": {
                    **CONTRACT_ATTRS_UC1_INIT,
                    "aggregateResult": {
                        "status": "INCONCLUSIVE",
                        "summary": "Verification in progress. Real-time lookup submitted to Parivahan Sewa. Result expected within PT30M.",
                    },
                    "expiresAt": "2026-08-12T10:30:00+05:30",
                },
            },
        },
    }

    status_body = {
        "context": ctx("status", MSG_UC1["status"], "2026-05-12T11:00:00+05:30"),
        "message": {
            "contract": {
                "id": "{{contract_id}}",
                "commitments": [{
                    "id": "commitment-uc1-dl-001",
                    "status": {"descriptor": {"code": "ACTIVE"}},
                    "resources": [dict(RESOURCE_DL_REF, **{"quantity": {"count": 1}})],
                    "offer": OFFER_DL_REF,
                }],
            },
        },
    }

    on_status_body = {
        "context": ctx("on_status", MSG_UC1["on_status"], "2026-05-12T11:00:02+05:30"),
        "message": {
            "contract": {
                "id": "{{contract_id}}",
                "status": {"code": "ACTIVE"},
                "descriptor": {
                    "name": "DL Verification — CityExpress / Ravi Kumar",
                    "shortDesc": "Verification complete — VERIFIED",
                },
                "commitments": [COMMITMENT_UC1_ACTIVE_FULL],
                "consideration": [cons_uc1("ACTIVE", {
                    "selectedPaymentMethod": "UPI",
                    "transactionRef": "{{payment_ref}}",
                })],
                "participants": [PARTICIPANT_UC1_FULL],
                "performance": [{
                    "id": "perf-uc1-dl-001",
                    "commitmentId": "commitment-uc1-dl-001",
                    "performanceAttributes": {
                        "@context": PERF_CTX,
                        "@type": "vp:VerificationPerformance",
                        "verificationResult": {
                            "status": "VERIFIED",
                            "matchScore": 0.98,
                            "remarks": "Licence details match Parivahan Sewa records. HMV endorsement active.",
                        },
                        "processingSteps": [
                            {"stepName": "INPUT_VALIDATION",  "status": "COMPLETED",
                             "timestamp": "2026-05-12T10:30:06+05:30"},
                            {"stepName": "SOURCE_QUERY",      "status": "COMPLETED",
                             "timestamp": "2026-05-12T10:30:08+05:30",
                             "details": "Parivahan Sewa API queried successfully"},
                            {"stepName": "DATA_COMPARISON",   "status": "COMPLETED",
                             "timestamp": "2026-05-12T10:30:09+05:30"},
                            {"stepName": "RESULT_COMPILATION","status": "COMPLETED",
                             "timestamp": "2026-05-12T10:30:10+05:30"},
                        ],
                        "verifiedData": {
                            "holderName":       "RAVI KUMAR",
                            "licenceNumber":    "KA0120190123456",
                            "issueDate":        "2019-03-20",
                            "expiryDate":       "2039-03-19",
                            "vehicleClasses":   "LMV, MCWG, HMV",
                            "issuingAuthority": "RTO Bengaluru Central (KA-01)",
                        },
                        "evidence": [{
                            "type":        "SOURCE_RESPONSE_HASH",
                            "hash":        "sha256-a3f8c2d1e4b9f70c5a2d6e8b1c4f7a0d3e6b9c2f5a8d1e4b7f0c3a6d9b2e5f8a",
                            "description": "SHA-256 hash of Parivahan Sewa API response for audit trail",
                            "createdAt":   "2026-05-12T10:30:08+05:30",
                        }],
                        "confidenceScore": 0.98,
                        "verifiedAt":      "2026-05-12T10:30:10+05:30",
                        "validUntil":      "2026-08-12T10:30:10+05:30",
                    },
                }],
                "contractAttributes": {
                    **CONTRACT_ATTRS_UC1_INIT,
                    "aggregateResult": {
                        "status":      "VERIFIED",
                        "summary":     "Driving licence KA0120190123456 verified against Parivahan Sewa. HMV endorsement confirmed active. Holder name matches.",
                        "completedAt": "2026-05-12T10:30:10+05:30",
                    },
                    "expiresAt": "2026-08-12T10:30:10+05:30",
                    "issuedCredentials": [{
                        "credentialId":       "cred-uc1-dl-001",
                        "credentialType":     "PDF",
                        "format":             "application/pdf",
                        "url":                "https://certs.trustverify.in/dl/cred-uc1-dl-001.pdf",
                        "issuedAt":           "2026-05-12T10:30:30+05:30",
                        "credentialExpiresAt":"2026-08-12T10:30:30+05:30",
                        "issuerId":           "{{provider_np_id}}",
                    }],
                },
                "settlements": [{
                    "id": "settlement-uc1-dl-001",
                    "considerationId": "cons-vs-dl-cat-001",
                    "status": "COMPLETE",
                }],
            },
        },
    }

    variables = [
        var("base_url",           "",                   "Provider NP (BPP) endpoint — set per environment"),
        var("requesting_np_uri",  "",                   "Requesting NP (BAP) callback URI — set per environment"),
        var("provider_np_uri",    "",                   "Provider NP (BPP) URI — set per environment"),
        var("requesting_np_id",   "cityexpress.in",     "Requesting NP network identifier (maps to bapId in Beckn context)"),
        var("provider_np_id",     "trustverify.in",     "Provider NP network identifier (maps to bppId in Beckn context)"),
        var("domain",             "vs:verification",    "Confirm exact domain prefix with network team"),
        var("network_id",         "vs.in/verification", "Confirm exact value with network registry team"),
        var("auth_token",         "",                   "Network-issued JWT — set before running"),
        var("transaction_id",     "c3d4e5f6-a7b8-4012-8d34-ef5678901aba", "UUID — regenerate for separate test runs"),
        var("contract_id",        "d4e5f6a7-b8c9-4123-8e45-fa6789012bcb", "Assigned by Provider NP at on_select"),
        var("payment_ref",        "UPI-20260512-103000-HDFC-001",         "UPI transaction reference"),
        var("subject_mobile_masked", "XXXXXXX4521",                       "Masked mobile for display — not shared in full"),
    ]

    folders = [
        folder("01 — discover",
               "Requesting NP (CityExpress) broadcasts intent to discover driving licence verification services.",
               [req("discover", "{{base_url}}/discover", discover_body,
                    "**discover** — Requesting NP → Gateway\n\n"
                    "CityExpress Bus Services broadcasts discovery intent filtering for "
                    "DRIVING_LICENCE verification resources. schemaContext included (catalog phase).")]),
        folder("02 — on_discover",
               "Provider NP (TrustVerify India) returns its full catalog with DL verification resource and offer.",
               [req("on_discover", "{{requesting_np_uri}}/on_discover", on_discover_body,
                    "**on_discover** — Provider NP → Requesting NP\n\n"
                    "TrustVerify India returns its full catalog. Requesting NP selects "
                    "`offer-vs-dl-std-001` (₹250/request, PT30M turnaround).")]),
        folder("03 — select",
               "Requesting NP originates the DRAFT contract selecting the DL verification offer.",
               [req("select", "{{base_url}}/select", select_body,
                    "**select** — Requesting NP → Provider NP\n\n"
                    "Requesting NP originates a DRAFT Contract selecting `offer-vs-dl-std-001` for "
                    "1 verification. No contract id yet — Provider NP assigns it at on_select. "
                    "Minimal participant (no PII at this stage). No contractAttributes — subject "
                    "will be introduced at init.")]),
        folder("04 — on_select",
               "Provider NP assigns contract id and returns PENDING pricing.",
               [req("on_select", "{{requesting_np_uri}}/on_select", on_select_body,
                    "**on_select** — Provider NP → Requesting NP\n\n"
                    "Provider NP assigns `{{contract_id}}` and returns PENDING consideration "
                    "(₹250). Requesting NP now has the contract id to use in all subsequent calls. "
                    "No contractAttributes — subject not yet in scope.")]),
        folder("05 — init",
               "Requesting NP submits full participant details, subject reference, purpose, and consent.",
               [req("init", "{{base_url}}/init", init_body,
                    "**init** — Requesting NP → Provider NP\n\n"
                    "Requesting NP introduces: (1) full organisation descriptor, "
                    "(2) contractAttributes with subject (Ravi Kumar), purpose "
                    "(EMPLOYMENT_ONBOARDING), and consent reference (OTP, granted 10:28 IST). "
                    "Consideration echoed as PENDING — binding intent signalled.")]),
        folder("06 — on_init",
               "Provider NP returns binding QUOTED consideration.",
               [req("on_init", "{{requesting_np_uri}}/on_init", on_init_body,
                    "**on_init** — Provider NP → Requesting NP\n\n"
                    "Provider NP returns QUOTED consideration (₹250 via UPI, UPFRONT). "
                    "Payment instructions are issued out-of-band. "
                    "Requesting NP proceeds to payment and then confirm.")]),
        folder("07 — confirm",
               "Requesting NP confirms the contract with payment authorisation.",
               [req("confirm", "{{base_url}}/confirm", confirm_body,
                    "**confirm** — Requesting NP → Provider NP\n\n"
                    "Requesting NP confirms the contract with ACTIVE consideration and "
                    "UPI payment authorisation. Contract status moves to ACTIVE. "
                    "Provider NP will begin the DL verification immediately.")]),
        folder("08 — on_confirm  ★ Verification Started",
               "Provider NP acknowledges payment and indicates verification is in progress (aggregateResult PENDING).",
               [req("on_confirm", "{{requesting_np_uri}}/on_confirm", on_confirm_body,
                    "**on_confirm** — Provider NP → Requesting NP\n\n"
                    "Contract is ACTIVE. Payment received. aggregateResult is INCONCLUSIVE "
                    "(verification submitted to Parivahan Sewa; PT30M SLA). "
                    "Requesting NP should poll via `status` after the SLA window.")]),
        folder("09 — status",
               "Requesting NP polls for verification result after PT30M.",
               [req("status", "{{base_url}}/status", status_body,
                    "**status** — Requesting NP → Provider NP\n\n"
                    "Poll for the verification result. Per core spec StatusAction, "
                    "message.contract carries the contract id and commitment refs "
                    "(not a flat message.contractId).")]),
        folder("10 — on_status  ★ Verification Complete",
               "Provider NP returns VERIFIED result with performance record and signed PDF certificate.",
               [req("on_status", "{{requesting_np_uri}}/on_status", on_status_body,
                    "**on_status** — Provider NP → Requesting NP\n\n"
                    "aggregateResult VERIFIED. Licence KA0120190123456 confirmed against "
                    "Parivahan Sewa (matchScore 0.98, HMV endorsement active). "
                    "issuedCredentials contains a signed PDF certificate valid for 90 days. "
                    "CityExpress can download the certificate from the URL and store it in "
                    "Ravi Kumar's onboarding record.")]),
    ]

    return col("VS — UC1: Bus Operator Driving Licence Verification", desc, variables, folders)


# =============================================================================
# COLLECTION 3 — UC2: EV FLEET DRIVER KYC (SYNCHRONOUS)
# =============================================================================

def build_uc2():
    desc = """\
## Verification Service Network — UC2: EV Fleet Driver KYC

**Scenario:** GreenMove EV Fleet Operations (Requesting NP) performs Aadhaar
eKYC on driver applicant Priya Sharma via IDVerify Solutions (Provider NP) for
KYC compliance before onboarding her to the fleet. Real-time UIDAI OTP flow;
result returned synchronously at on_confirm within PT5M.

**Protocol:** Beckn v2.0.0 + Verification Service schema pack v2.1.0
**Verification type:** IDENTITY (Aadhaar eKYC) | **Method:** REAL_TIME_API | **Turnaround:** PT5M
**Purpose:** KYC_COMPLIANCE | **Consent:** AADHAAR_EKYC

### Structural conventions

- Synchronous flow — aggregateResult VERIFIED already at on_confirm
- issuedCredentials (W3C VC) present in on_confirm contractAttributes
- on_status confirms the stable VERIFIED state and records the settlement
- Subject (Priya Sharma) introduced at init under Aadhaar eKYC consent

### Consideration lifecycle

| Call | status.code | price |
|---|---|---|
| catalog (on_discover) | *(none)* | ₹150 |
| on_select | PENDING | ₹150 |
| init | PENDING | ₹150 |
| on_init | QUOTED | ₹150 |
| confirm / on_confirm / on_status | ACTIVE | ₹150 |

### Quick-start: environment setup

1. Import **VS_Environment.json** and select the environment.
2. Set `base_url`, `requesting_np_uri`, `provider_np_uri`, and `auth_token`.
3. Run folders 01–10 in order.
"""

    COMMITMENT_UC2_DRAFT_REF = {
        "id": "commitment-uc2-identity-001",
        "status": {"descriptor": {"code": "DRAFT"}},
        "resources": [dict(RESOURCE_IDENTITY_REF, **{"quantity": {"count": 1}})],
        "offer": OFFER_IDENTITY_REF,
    }

    COMMITMENT_UC2_DRAFT_FULL = {
        "id": "commitment-uc2-identity-001",
        "status": {"descriptor": {"code": "DRAFT"}},
        "resources": [dict(RESOURCE_IDENTITY_FULL, **{"quantity": {"count": 1}})],
        "offer": OFFER_IDENTITY_FULL,
    }

    COMMITMENT_UC2_ACTIVE_REF = {
        "id": "commitment-uc2-identity-001",
        "status": {"descriptor": {"code": "ACTIVE"}},
        "resources": [dict(RESOURCE_IDENTITY_REF, **{"quantity": {"count": 1}})],
        "offer": OFFER_IDENTITY_REF,
    }

    COMMITMENT_UC2_ACTIVE_FULL = {
        "id": "commitment-uc2-identity-001",
        "status": {"descriptor": {"code": "ACTIVE"}},
        "resources": [dict(RESOURCE_IDENTITY_FULL, **{"quantity": {"count": 1}})],
        "offer": OFFER_IDENTITY_FULL,
    }

    PARTICIPANT_UC2_MINIMAL = {"id": "part-uc2-greenmove-001"}

    PARTICIPANT_UC2_FULL = {
        "id": "part-uc2-greenmove-001",
        "role": "REQUESTER",
        "descriptor": {
            "name":      "GreenMove EV Fleet Operations Pvt. Ltd.",
            "shortDesc": "Requesting NP — EV fleet operator, Pune",
        },
    }

    def cons_uc2(status_code, extra=None):
        attrs = {
            "@type": "schema:PriceSpecification",
            "price": 150, "priceCurrency": "INR",
            "valueAddedTaxIncluded": False,
            "description": "Per-request Aadhaar eKYC fee, excluding GST",
        }
        if extra:
            attrs.update(extra)
        return {
            "id": "cons-vs-identity-cat-001",
            "status": {"code": status_code},
            "considerationAttributes": attrs,
        }

    CONTRACT_ATTRS_UC2_INIT = {
        "@context": CONTRACT_CTX,
        "@type": "vc:VerificationContract",
        "subject": {
            "name": "Priya Sharma",
            "dateOfBirth": "1998-07-22",
            "identifiers": [
                {"type": "AADHAAR", "value": "{{aadhaar_ref}}",
                 "maskedValue": "XXXX-XXXX-4567"},
                {"type": "MOBILE",  "value": "{{subject_mobile_masked}}",
                 "maskedValue": "XXXXXXX8832"},
            ],
        },
        "purpose": {
            "code": "KYC_COMPLIANCE",
            "description": "Aadhaar eKYC for EV fleet driver onboarding compliance",
        },
        "consentReference": {
            "consentId": "consent-uc2-ps-001",
            "mechanism": "AADHAAR_EKYC",
            "grantedAt": "2026-05-15T14:10:00+05:30",
            "expiresAt": "2026-05-15T15:10:00+05:30",
            "scope": ["IDENTITY"],
        },
        "requestedBy": {
            "organizationName": "GreenMove EV Fleet Operations Pvt. Ltd.",
            "organizationType": "EMPLOYER",
            "referenceId": "driver-application-gm-2026-0515-007",
        },
    }

    PERF_UC2 = {
        "id": "perf-uc2-identity-001",
        "commitmentId": "commitment-uc2-identity-001",
        "performanceAttributes": {
            "@context": PERF_CTX,
            "@type": "vp:VerificationPerformance",
            "verificationResult": {
                "status":    "VERIFIED",
                "matchScore": 1.0,
                "remarks":   "Identity verified against UIDAI Aadhaar database. OTP consent confirmed.",
            },
            "processingSteps": [
                {"stepName": "INPUT_VALIDATION", "status": "COMPLETED",
                 "timestamp": "2026-05-15T14:12:01+05:30"},
                {"stepName": "SOURCE_QUERY",     "status": "COMPLETED",
                 "timestamp": "2026-05-15T14:12:03+05:30",
                 "details": "UIDAI eKYC API called; OTP verified"},
                {"stepName": "DATA_EXTRACTION",  "status": "COMPLETED",
                 "timestamp": "2026-05-15T14:12:04+05:30"},
                {"stepName": "RESULT_COMPILATION","status": "COMPLETED",
                 "timestamp": "2026-05-15T14:12:05+05:30"},
            ],
            "verifiedData": {
                "name":        "PRIYA SHARMA",
                "dateOfBirth": "1998-07-22",
                "gender":      "F",
                "address": {
                    "house": "Flat 204", "street": "Koregaon Park",
                    "city": "Pune", "state": "MH", "pincode": "411001",
                },
            },
            "evidence": [{
                "type":        "SOURCE_RESPONSE_HASH",
                "hash":        "sha256-b7c3e1f5a9d2b6e0c4f8a2d5b9c3e7f1a5d9b3e7c1f5a9d3b7e1f5a9c3d7b1e5",
                "description": "SHA-256 hash of UIDAI eKYC API response",
                "createdAt":   "2026-05-15T14:12:04+05:30",
            }],
            "confidenceScore": 1.0,
            "verifiedAt":      "2026-05-15T14:12:05+05:30",
            "validUntil":      "2027-05-15T14:12:05+05:30",
        },
    }

    ISSUED_CRED_UC2 = {
        "credentialId":       "cred-uc2-identity-001",
        "credentialType":     "W3C_VC",
        "format":             "application/ld+json",
        "url":                "https://certs.idverify.in/vc/cred-uc2-identity-001",
        "issuedAt":           "2026-05-15T14:12:10+05:30",
        "credentialExpiresAt":"2027-05-15T14:12:10+05:30",
        "issuerId":           "{{provider_np_id}}",
    }

    discover_body = {
        "context": ctx("discover", MSG_UC2["discover"], "2026-05-15T14:05:00+05:30",
                       include_bpp=False, schema_contexts=SCHEMA_CTX_CATALOG),
        "message": {
            "intent": {
                "filters": "$.catalogs[*].resources[*] ? (@.resourceAttributes.verificationType.code == \"IDENTITY\")",
                "textSearch": "Aadhaar eKYC",
            },
        },
    }

    on_discover_body = {
        "context": ctx("on_discover", MSG_UC2["on_discover"], "2026-05-15T14:05:04+05:30",
                       schema_contexts=SCHEMA_CTX_CATALOG),
        "message": {
            "catalogs": [{
                "id": "cat-vs-idverify-001",
                "descriptor": {
                    "name":      "IDVerify Solutions — Verification Service Catalog",
                    "shortDesc": "Identity and Aadhaar eKYC verification for the mobility sector",
                },
                "provider": {
                    "id": "{{provider_np_id}}",
                    "descriptor": {
                        "name":      "IDVerify Solutions Pvt. Ltd.",
                        "shortDesc": "UIDAI-authorised AUA; DPDPA 2023 compliant",
                    },
                },
                "resources": [RESOURCE_IDENTITY_FULL],
                "offers":    [OFFER_IDENTITY_FULL],
            }],
        },
    }

    select_body = {
        "context": ctx("select", MSG_UC2["select"], "2026-05-15T14:10:00+05:30"),
        "message": {
            "contract": {
                "status": {"code": "DRAFT"},
                "commitments": [COMMITMENT_UC2_DRAFT_REF],
                "participants": [PARTICIPANT_UC2_MINIMAL],
            },
        },
    }

    on_select_body = {
        "context": ctx("on_select", MSG_UC2["on_select"], "2026-05-15T14:10:02+05:30"),
        "message": {
            "contract": {
                "id": "{{contract_id}}",
                "status": {"code": "DRAFT"},
                "commitments": [COMMITMENT_UC2_DRAFT_FULL],
                "consideration": [cons_uc2("PENDING")],
                "participants": [PARTICIPANT_UC2_MINIMAL],
            },
        },
    }

    init_body = {
        "context": ctx("init", MSG_UC2["init"], "2026-05-15T14:11:00+05:30"),
        "message": {
            "contract": {
                "id": "{{contract_id}}",
                "status": {"code": "DRAFT"},
                "commitments": [COMMITMENT_UC2_DRAFT_REF],
                "consideration": [cons_uc2("PENDING")],
                "participants": [PARTICIPANT_UC2_FULL],
                "contractAttributes": CONTRACT_ATTRS_UC2_INIT,
            },
        },
    }

    on_init_body = {
        "context": ctx("on_init", MSG_UC2["on_init"], "2026-05-15T14:11:02+05:30"),
        "message": {
            "contract": {
                "id": "{{contract_id}}",
                "status": {"code": "DRAFT"},
                "commitments": [COMMITMENT_UC2_DRAFT_FULL],
                "consideration": [cons_uc2("QUOTED", {
                    "selectedPaymentMethod": "UPI",
                    "paymentSchedule": "UPFRONT",
                })],
                "participants": [PARTICIPANT_UC2_FULL],
                "contractAttributes": CONTRACT_ATTRS_UC2_INIT,
            },
        },
    }

    confirm_body = {
        "context": ctx("confirm", MSG_UC2["confirm"], "2026-05-15T14:12:00+05:30"),
        "message": {
            "contract": {
                "id": "{{contract_id}}",
                "status": {"code": "ACTIVE"},
                "commitments": [COMMITMENT_UC2_ACTIVE_REF],
                "consideration": [cons_uc2("ACTIVE", {
                    "selectedPaymentMethod": "UPI",
                    "transactionRef": "{{payment_ref}}",
                    "paymentAuthorisation": {
                        "authCode": "{{payment_ref}}",
                        "authProvider": "ICICI_UPI",
                        "authTimestamp": "2026-05-15T14:11:58+05:30",
                        "authAmount": 150,
                    },
                })],
                "participants": [PARTICIPANT_UC2_FULL],
                "contractAttributes": CONTRACT_ATTRS_UC2_INIT,
            },
        },
    }

    on_confirm_body = {
        "context": ctx("on_confirm", MSG_UC2["on_confirm"], "2026-05-15T14:12:10+05:30"),
        "message": {
            "contract": {
                "id": "{{contract_id}}",
                "status": {"code": "ACTIVE"},
                "descriptor": {
                    "name":      "Identity KYC — GreenMove / Priya Sharma",
                    "shortDesc": "Aadhaar eKYC verified — VERIFIED",
                },
                "commitments": [COMMITMENT_UC2_ACTIVE_FULL],
                "consideration": [cons_uc2("ACTIVE", {
                    "selectedPaymentMethod": "UPI",
                    "transactionRef": "{{payment_ref}}",
                })],
                "participants": [PARTICIPANT_UC2_FULL],
                "performance": [PERF_UC2],
                "contractAttributes": {
                    **CONTRACT_ATTRS_UC2_INIT,
                    "aggregateResult": {
                        "status":      "VERIFIED",
                        "summary":     "Identity verified against UIDAI Aadhaar. Name, date of birth, gender, and address confirmed. OTP consent validated.",
                        "completedAt": "2026-05-15T14:12:05+05:30",
                    },
                    "expiresAt":        "2027-05-15T14:12:10+05:30",
                    "issuedCredentials": [ISSUED_CRED_UC2],
                },
                "settlements": [{
                    "id": "settlement-uc2-identity-001",
                    "considerationId": "cons-vs-identity-cat-001",
                    "status": "COMPLETE",
                }],
            },
        },
    }

    status_body = {
        "context": ctx("status", MSG_UC2["status"], "2026-05-15T14:15:00+05:30"),
        "message": {
            "contract": {
                "id": "{{contract_id}}",
                "commitments": [{
                    "id": "commitment-uc2-identity-001",
                    "status": {"descriptor": {"code": "ACTIVE"}},
                    "resources": [dict(RESOURCE_IDENTITY_REF, **{"quantity": {"count": 1}})],
                    "offer": OFFER_IDENTITY_REF,
                }],
            },
        },
    }

    on_status_body = {
        "context": ctx("on_status", MSG_UC2["on_status"], "2026-05-15T14:15:02+05:30"),
        "message": {
            "contract": {
                "id": "{{contract_id}}",
                "status": {"code": "ACTIVE"},
                "descriptor": {
                    "name":      "Identity KYC — GreenMove / Priya Sharma",
                    "shortDesc": "Verification complete and stable — VERIFIED",
                },
                "commitments": [COMMITMENT_UC2_ACTIVE_FULL],
                "consideration": [cons_uc2("ACTIVE", {
                    "selectedPaymentMethod": "UPI",
                    "transactionRef": "{{payment_ref}}",
                })],
                "participants": [PARTICIPANT_UC2_FULL],
                "performance": [PERF_UC2],
                "contractAttributes": {
                    **CONTRACT_ATTRS_UC2_INIT,
                    "aggregateResult": {
                        "status":      "VERIFIED",
                        "summary":     "Identity verified against UIDAI Aadhaar. Stable result. W3C VC credential issued.",
                        "completedAt": "2026-05-15T14:12:05+05:30",
                    },
                    "expiresAt":        "2027-05-15T14:12:10+05:30",
                    "issuedCredentials": [ISSUED_CRED_UC2],
                },
                "settlements": [{
                    "id": "settlement-uc2-identity-001",
                    "considerationId": "cons-vs-identity-cat-001",
                    "status": "COMPLETE",
                }],
            },
        },
    }

    variables = [
        var("base_url",           "",                    "Provider NP (BPP) endpoint — set per environment"),
        var("requesting_np_uri",  "",                    "Requesting NP (BAP) callback URI — set per environment"),
        var("provider_np_uri",    "",                    "Provider NP (BPP) URI — set per environment"),
        var("requesting_np_id",   "greenmove-ev.in",     "Requesting NP network identifier (maps to bapId in Beckn context)"),
        var("provider_np_id",     "idverify.in",         "Provider NP network identifier (maps to bppId in Beckn context)"),
        var("domain",             "vs:verification",     "Confirm exact domain prefix with network team"),
        var("network_id",         "vs.in/verification",  "Confirm exact value with network registry team"),
        var("auth_token",         "",                    "Network-issued JWT — set before running"),
        var("transaction_id",     "a3b4c5d6-e7f8-4012-8b34-cd5678901ef2", "UUID — regenerate for separate test runs"),
        var("contract_id",        "b4c5d6e7-f8a9-4123-8c45-de6789012fa3", "Assigned by Provider NP at on_select"),
        var("payment_ref",        "UPI-20260515-141200-ICICI-007",        "UPI transaction reference"),
        var("aadhaar_ref",        "{{aadhaar_ref}}",     "Aadhaar number — never store plaintext; handle server-side"),
        var("subject_mobile_masked", "XXXXXXX8832",      "Masked mobile for display only"),
    ]

    folders = [
        folder("01 — discover",
               "Requesting NP (GreenMove) discovers identity verification services.",
               [req("discover", "{{base_url}}/discover", discover_body,
                    "**discover** — Requesting NP → Gateway\n\n"
                    "GreenMove EV Fleet Operations filters for IDENTITY verification resources "
                    "with textSearch hint 'Aadhaar eKYC'. schemaContext included (catalog phase).")]),
        folder("02 — on_discover",
               "Provider NP (IDVerify Solutions) returns its identity verification catalog.",
               [req("on_discover", "{{requesting_np_uri}}/on_discover", on_discover_body,
                    "**on_discover** — Provider NP → Requesting NP\n\n"
                    "IDVerify Solutions returns its catalog. Requesting NP selects "
                    "`offer-vs-identity-instant-001` (₹150/request, PT5M, PREMIUM tier).")]),
        folder("03 — select",
               "Requesting NP originates DRAFT contract for the identity verification offer.",
               [req("select", "{{base_url}}/select", select_body,
                    "**select** — Requesting NP → Provider NP\n\n"
                    "DRAFT Contract with identity commitment (1 verification). Minimal "
                    "participant at this stage — no PII, no subject reference yet.")]),
        folder("04 — on_select",
               "Provider NP assigns contract id and returns PENDING pricing.",
               [req("on_select", "{{requesting_np_uri}}/on_select", on_select_body,
                    "**on_select** — Provider NP → Requesting NP\n\n"
                    "Provider NP assigns `{{contract_id}}`. PENDING consideration ₹150.")]),
        folder("05 — init",
               "Requesting NP submits Aadhaar eKYC subject reference, purpose, and consent.",
               [req("init", "{{base_url}}/init", init_body,
                    "**init** — Requesting NP → Provider NP\n\n"
                    "Requesting NP introduces subject (Priya Sharma, masked Aadhaar), purpose "
                    "(KYC_COMPLIANCE), and Aadhaar eKYC consent reference. "
                    "The actual Aadhaar number is handled server-side — only masked reference "
                    "and the consent token flow through the Beckn message.")]),
        folder("06 — on_init",
               "Provider NP returns QUOTED consideration.",
               [req("on_init", "{{requesting_np_uri}}/on_init", on_init_body,
                    "**on_init** — Provider NP → Requesting NP\n\n"
                    "QUOTED consideration (₹150 UPI UPFRONT). Payment instructions out-of-band.")]),
        folder("07 — confirm",
               "Requesting NP confirms the contract with payment authorisation.",
               [req("confirm", "{{base_url}}/confirm", confirm_body,
                    "**confirm** — Requesting NP → Provider NP\n\n"
                    "ACTIVE consideration with ICICI UPI payment authorisation (₹150). "
                    "Provider NP initiates real-time Aadhaar eKYC immediately on receipt.")]),
        folder("08 — on_confirm  ★ KYC Verified (Synchronous)",
               "Provider NP returns VERIFIED result synchronously — KYC complete at on_confirm.",
               [req("on_confirm", "{{requesting_np_uri}}/on_confirm", on_confirm_body,
                    "**on_confirm** — Provider NP → Requesting NP\n\n"
                    "Synchronous result: aggregateResult VERIFIED within PT5M SLA. "
                    "Performance record included (UIDAI eKYC response hash as evidence). "
                    "issuedCredentials carries a W3C VC pointing to the signed KYC certificate. "
                    "GreenMove can immediately proceed with driver onboarding.")]),
        folder("09 — status",
               "Requesting NP polls to confirm stable state (optional for sync use cases).",
               [req("status", "{{base_url}}/status", status_body,
                    "**status** — Requesting NP → Provider NP\n\n"
                    "Status poll to confirm the stable VERIFIED state and retrieve "
                    "the final settlement record. Optional for synchronous use cases "
                    "where on_confirm already carries the result.")]),
        folder("10 — on_status  ★ Stable Verified State",
               "Provider NP confirms VERIFIED state with settlement record.",
               [req("on_status", "{{requesting_np_uri}}/on_status", on_status_body,
                    "**on_status** — Provider NP → Requesting NP\n\n"
                    "Stable VERIFIED result with settlement COMPLETE. "
                    "W3C VC credential valid for 1 year (credentialExpiresAt 2027-05-15).")]),
    ]

    return col("VS — UC2: EV Fleet Driver KYC (Aadhaar eKYC)", desc, variables, folders)


# =============================================================================
# COLLECTION 4 — UC4: EV TECH SKILL CERTIFICATE VERIFICATION
# =============================================================================

def build_uc4():
    desc = """\
## Verification Service Network — UC4: EV Fleet Tech Skill Certificate Verification

**Scenario:** ZapCharge Fleet Services (Requesting NP) verifies the NSDC EV
Technology certificate of technician applicant Arjun Mehta via CertVerify India
(Provider NP) before onboarding him to their EV fleet maintenance platform.
Hybrid verification (automated Skill India portal lookup + manual review);
result available within 1 business day. on_confirm indicates verification in
progress (PENDING); on_status returns VERIFIED with a signed PDF certificate.

**Protocol:** Beckn v2.0.0 + Verification Service schema pack v2.1.0
**Verification type:** SKILL_CERTIFICATE | **Method:** HYBRID | **Turnaround:** P1D
**Purpose:** PLATFORM_ONBOARDING | **Consent:** OTP

### Structural conventions

- Async hybrid flow — aggregateResult INCONCLUSIVE at on_confirm (P1D SLA)
- on_status returns VERIFIED + performance record (confidence 0.95) + signed PDF
- HYBRID method: automated Skill India portal lookup + manual review step

### Consideration lifecycle

| Call | status.code | price |
|---|---|---|
| catalog (on_discover) | *(none)* | ₹350 |
| on_select | PENDING | ₹350 |
| init | PENDING | ₹350 |
| on_init | QUOTED | ₹350 |
| confirm / on_confirm / on_status | ACTIVE | ₹350 |

### Quick-start: environment setup

1. Import **VS_Environment.json** and select the environment.
2. Set `base_url`, `requesting_np_uri`, `provider_np_uri`, and `auth_token`.
3. Run folders 01–10 in order. After confirm, wait P1D before polling status.
"""

    COMMITMENT_UC4_DRAFT_REF = {
        "id": "commitment-uc4-skill-001",
        "status": {"descriptor": {"code": "DRAFT"}},
        "resources": [dict(RESOURCE_SKILL_REF, **{"quantity": {"count": 1}})],
        "offer": OFFER_SKILL_REF,
    }

    COMMITMENT_UC4_DRAFT_FULL = {
        "id": "commitment-uc4-skill-001",
        "status": {"descriptor": {"code": "DRAFT"}},
        "resources": [dict(RESOURCE_SKILL_FULL, **{"quantity": {"count": 1}})],
        "offer": OFFER_SKILL_FULL,
    }

    COMMITMENT_UC4_ACTIVE_REF = {
        "id": "commitment-uc4-skill-001",
        "status": {"descriptor": {"code": "ACTIVE"}},
        "resources": [dict(RESOURCE_SKILL_REF, **{"quantity": {"count": 1}})],
        "offer": OFFER_SKILL_REF,
    }

    COMMITMENT_UC4_ACTIVE_FULL = {
        "id": "commitment-uc4-skill-001",
        "status": {"descriptor": {"code": "ACTIVE"}},
        "resources": [dict(RESOURCE_SKILL_FULL, **{"quantity": {"count": 1}})],
        "offer": OFFER_SKILL_FULL,
    }

    PARTICIPANT_UC4_MINIMAL = {"id": "part-uc4-zapcharge-001"}

    PARTICIPANT_UC4_FULL = {
        "id": "part-uc4-zapcharge-001",
        "role": "REQUESTER",
        "descriptor": {
            "name":      "ZapCharge Fleet Services Pvt. Ltd.",
            "shortDesc": "Requesting NP — EV fleet technology services provider, Hyderabad",
        },
    }

    def cons_uc4(status_code, extra=None):
        attrs = {
            "@type": "schema:PriceSpecification",
            "price": 350, "priceCurrency": "INR",
            "valueAddedTaxIncluded": False,
            "description": "Per-request skill certificate verification fee, excluding GST",
        }
        if extra:
            attrs.update(extra)
        return {
            "id": "cons-vs-skill-cat-001",
            "status": {"code": status_code},
            "considerationAttributes": attrs,
        }

    CONTRACT_ATTRS_UC4_INIT = {
        "@context": CONTRACT_CTX,
        "@type": "vc:VerificationContract",
        "subject": {
            "name": "Arjun Mehta",
            "dateOfBirth": "1995-11-08",
            "identifiers": [
                {"type": "EMPLOYEE_ID",  "value": "AM-ZC-2026-0045",
                 "maskedValue": "AM-ZC-2026-0045"},
                {"type": "MOBILE",       "value": "{{subject_mobile_masked}}",
                 "maskedValue": "XXXXXXX2217"},
            ],
        },
        "purpose": {
            "code": "PLATFORM_ONBOARDING",
            "description": "Skill certificate verification for EV fleet technician platform onboarding",
        },
        "consentReference": {
            "consentId": "consent-uc4-am-001",
            "mechanism": "OTP",
            "grantedAt": "2026-05-20T09:30:00+05:30",
            "expiresAt": "2026-05-20T10:30:00+05:30",
            "scope": ["SKILL_CERTIFICATE"],
        },
        "requestedBy": {
            "organizationName": "ZapCharge Fleet Services Pvt. Ltd.",
            "organizationType": "PLATFORM",
            "referenceId": "tech-application-zc-2026-0520-045",
        },
    }

    CONTRACT_ATTRS_UC4_CERT_INPUT = {
        **CONTRACT_ATTRS_UC4_INIT,
        "certificateInput": {
            "certificateNumber": "NSDC-EV-2024-78901",
            "holderName":        "Arjun Mehta",
            "issuingBody":       "ASDC — Automotive Skills Development Council",
            "issueYear":         2024,
        },
    }

    discover_body = {
        "context": ctx("discover", MSG_UC4["discover"], "2026-05-20T09:15:00+05:30",
                       include_bpp=False, schema_contexts=SCHEMA_CTX_CATALOG),
        "message": {
            "intent": {
                "filters": "$.catalogs[*].resources[*] ? (@.resourceAttributes.verificationType.code == \"SKILL_CERTIFICATE\")",
                "textSearch": "NSDC EV technology certificate",
            },
        },
    }

    on_discover_body = {
        "context": ctx("on_discover", MSG_UC4["on_discover"], "2026-05-20T09:15:04+05:30",
                       schema_contexts=SCHEMA_CTX_CATALOG),
        "message": {
            "catalogs": [{
                "id": "cat-vs-certverify-001",
                "descriptor": {
                    "name":      "CertVerify India — Skill Certificate Verification Catalog",
                    "shortDesc": "NSDC and Sector Skill Council certificate verification",
                },
                "provider": {
                    "id": "{{provider_np_id}}",
                    "descriptor": {
                        "name":      "CertVerify India Pvt. Ltd.",
                        "shortDesc": "Accredited by NSDC for digital certificate verification",
                    },
                },
                "resources": [RESOURCE_SKILL_FULL],
                "offers":    [OFFER_SKILL_FULL],
            }],
        },
    }

    select_body = {
        "context": ctx("select", MSG_UC4["select"], "2026-05-20T09:30:00+05:30"),
        "message": {
            "contract": {
                "status": {"code": "DRAFT"},
                "commitments": [COMMITMENT_UC4_DRAFT_REF],
                "participants": [PARTICIPANT_UC4_MINIMAL],
            },
        },
    }

    on_select_body = {
        "context": ctx("on_select", MSG_UC4["on_select"], "2026-05-20T09:30:02+05:30"),
        "message": {
            "contract": {
                "id": "{{contract_id}}",
                "status": {"code": "DRAFT"},
                "commitments": [COMMITMENT_UC4_DRAFT_FULL],
                "consideration": [cons_uc4("PENDING")],
                "participants": [PARTICIPANT_UC4_MINIMAL],
            },
        },
    }

    init_body = {
        "context": ctx("init", MSG_UC4["init"], "2026-05-20T09:31:00+05:30"),
        "message": {
            "contract": {
                "id": "{{contract_id}}",
                "status": {"code": "DRAFT"},
                "commitments": [COMMITMENT_UC4_DRAFT_REF],
                "consideration": [cons_uc4("PENDING")],
                "participants": [PARTICIPANT_UC4_FULL],
                "contractAttributes": CONTRACT_ATTRS_UC4_CERT_INPUT,
            },
        },
    }

    on_init_body = {
        "context": ctx("on_init", MSG_UC4["on_init"], "2026-05-20T09:31:02+05:30"),
        "message": {
            "contract": {
                "id": "{{contract_id}}",
                "status": {"code": "DRAFT"},
                "commitments": [COMMITMENT_UC4_DRAFT_FULL],
                "consideration": [cons_uc4("QUOTED", {
                    "selectedPaymentMethod": "NEFT",
                    "paymentSchedule": "UPFRONT",
                })],
                "participants": [PARTICIPANT_UC4_FULL],
                "contractAttributes": CONTRACT_ATTRS_UC4_CERT_INPUT,
            },
        },
    }

    confirm_body = {
        "context": ctx("confirm", MSG_UC4["confirm"], "2026-05-20T09:32:00+05:30"),
        "message": {
            "contract": {
                "id": "{{contract_id}}",
                "status": {"code": "ACTIVE"},
                "commitments": [COMMITMENT_UC4_ACTIVE_REF],
                "consideration": [cons_uc4("ACTIVE", {
                    "selectedPaymentMethod": "NEFT",
                    "transactionRef": "{{payment_ref}}",
                    "paymentAuthorisation": {
                        "authCode": "{{payment_ref}}",
                        "authProvider": "AXIS_BANK",
                        "authTimestamp": "2026-05-20T09:31:50+05:30",
                        "authAmount": 350,
                    },
                })],
                "participants": [PARTICIPANT_UC4_FULL],
                "contractAttributes": CONTRACT_ATTRS_UC4_CERT_INPUT,
            },
        },
    }

    on_confirm_body = {
        "context": ctx("on_confirm", MSG_UC4["on_confirm"], "2026-05-20T09:32:05+05:30"),
        "message": {
            "contract": {
                "id": "{{contract_id}}",
                "status": {"code": "ACTIVE"},
                "descriptor": {
                    "name":      "Skill Cert Verification — ZapCharge / Arjun Mehta",
                    "shortDesc": "Hybrid verification in progress — result by EOD 2026-05-21",
                },
                "commitments": [COMMITMENT_UC4_ACTIVE_FULL],
                "consideration": [cons_uc4("ACTIVE", {
                    "selectedPaymentMethod": "NEFT",
                    "transactionRef": "{{payment_ref}}",
                })],
                "participants": [PARTICIPANT_UC4_FULL],
                "contractAttributes": {
                    **CONTRACT_ATTRS_UC4_CERT_INPUT,
                    "aggregateResult": {
                        "status":  "INCONCLUSIVE",
                        "summary": "Verification in progress. Skill India portal queried; manual review queued for certificates not yet in digital registry. Result expected by EOD 2026-05-21 (P1D SLA).",
                    },
                    "expiresAt": "2026-11-20T09:32:00+05:30",
                },
            },
        },
    }

    status_body = {
        "context": ctx("status", MSG_UC4["status"], "2026-05-21T10:00:00+05:30"),
        "message": {
            "contract": {
                "id": "{{contract_id}}",
                "commitments": [{
                    "id": "commitment-uc4-skill-001",
                    "status": {"descriptor": {"code": "ACTIVE"}},
                    "resources": [dict(RESOURCE_SKILL_REF, **{"quantity": {"count": 1}})],
                    "offer": OFFER_SKILL_REF,
                }],
            },
        },
    }

    on_status_body = {
        "context": ctx("on_status", MSG_UC4["on_status"], "2026-05-21T10:00:03+05:30"),
        "message": {
            "contract": {
                "id": "{{contract_id}}",
                "status": {"code": "ACTIVE"},
                "descriptor": {
                    "name":      "Skill Cert Verification — ZapCharge / Arjun Mehta",
                    "shortDesc": "Verification complete — VERIFIED",
                },
                "commitments": [COMMITMENT_UC4_ACTIVE_FULL],
                "consideration": [cons_uc4("ACTIVE", {
                    "selectedPaymentMethod": "NEFT",
                    "transactionRef": "{{payment_ref}}",
                })],
                "participants": [PARTICIPANT_UC4_FULL],
                "performance": [{
                    "id": "perf-uc4-skill-001",
                    "commitmentId": "commitment-uc4-skill-001",
                    "performanceAttributes": {
                        "@context": PERF_CTX,
                        "@type": "vp:VerificationPerformance",
                        "verificationResult": {
                            "status":    "VERIFIED",
                            "matchScore": 0.95,
                            "remarks":   "NSDC-EV-2024-78901 found in Skill India portal. Manual review confirmed ASDC EV Technology QP:ASC/Q1412 Level 4.",
                        },
                        "processingSteps": [
                            {"stepName": "INPUT_VALIDATION", "status": "COMPLETED",
                             "timestamp": "2026-05-20T09:32:10+05:30"},
                            {"stepName": "SOURCE_QUERY",     "status": "COMPLETED",
                             "timestamp": "2026-05-20T09:32:15+05:30",
                             "details": "Skill India portal returned certificate record"},
                            {"stepName": "DATA_EXTRACTION",  "status": "COMPLETED",
                             "timestamp": "2026-05-20T09:32:16+05:30"},
                            {"stepName": "MANUAL_REVIEW",    "status": "COMPLETED",
                             "timestamp": "2026-05-21T09:45:00+05:30",
                             "details": "Reviewer confirmed ASDC issuing body and QP code"},
                            {"stepName": "RESULT_COMPILATION","status": "COMPLETED",
                             "timestamp": "2026-05-21T09:50:00+05:30"},
                        ],
                        "verifiedData": {
                            "holderName":        "ARJUN MEHTA",
                            "certificateNumber": "NSDC-EV-2024-78901",
                            "skillName":         "EV Technology — Maintenance and Repair",
                            "qualificationPack": "ASC/Q1412",
                            "issuingBody":       "ASDC — Automotive Skills Development Council",
                            "issueDate":         "2024-09-15",
                            "expiryDate":        "2027-09-14",
                        },
                        "evidence": [
                            {
                                "type":        "SOURCE_RESPONSE_HASH",
                                "hash":        "sha256-f1e2d3c4b5a6f7e8d9c0b1a2f3e4d5c6b7a8f9e0d1c2b3a4f5e6d7c8b9a0f1e2",
                                "description": "SHA-256 hash of Skill India portal API response",
                                "createdAt":   "2026-05-20T09:32:15+05:30",
                            },
                            {
                                "type":        "MANUAL_REVIEW_NOTES",
                                "description": "Manual reviewer notes confirming ASDC issuing body; internal case ID CVR-2026-0520-089",
                                "createdAt":   "2026-05-21T09:45:00+05:30",
                            },
                        ],
                        "confidenceScore": 0.95,
                        "verifiedAt":      "2026-05-21T09:50:00+05:30",
                        "validUntil":      "2026-11-21T09:50:00+05:30",
                    },
                }],
                "contractAttributes": {
                    **CONTRACT_ATTRS_UC4_CERT_INPUT,
                    "aggregateResult": {
                        "status":      "VERIFIED",
                        "summary":     "NSDC-EV-2024-78901 verified. EV Technology QP:ASC/Q1412 Level 4 confirmed active. Manual review complete.",
                        "completedAt": "2026-05-21T09:50:00+05:30",
                    },
                    "expiresAt": "2026-11-20T09:32:00+05:30",
                    "issuedCredentials": [{
                        "credentialId":       "cred-uc4-skill-001",
                        "credentialType":     "PDF",
                        "format":             "application/pdf",
                        "url":                "https://certs.certverify.in/skill/cred-uc4-skill-001.pdf",
                        "issuedAt":           "2026-05-21T09:55:00+05:30",
                        "credentialExpiresAt":"2026-11-21T09:55:00+05:30",
                        "issuerId":           "{{provider_np_id}}",
                    }],
                },
                "settlements": [{
                    "id": "settlement-uc4-skill-001",
                    "considerationId": "cons-vs-skill-cat-001",
                    "status": "COMPLETE",
                }],
            },
        },
    }

    variables = [
        var("base_url",           "",                    "Provider NP (BPP) endpoint — set per environment"),
        var("requesting_np_uri",  "",                    "Requesting NP (BAP) callback URI — set per environment"),
        var("provider_np_uri",    "",                    "Provider NP (BPP) URI — set per environment"),
        var("requesting_np_id",   "zapcharge.in",        "Requesting NP network identifier (maps to bapId in Beckn context)"),
        var("provider_np_id",     "certverify.in",       "Provider NP network identifier (maps to bppId in Beckn context)"),
        var("domain",             "vs:verification",     "Confirm exact domain prefix with network team"),
        var("network_id",         "vs.in/verification",  "Confirm exact value with network registry team"),
        var("auth_token",         "",                    "Network-issued JWT — set before running"),
        var("transaction_id",     "e3f4a5b6-c7d8-4012-8f34-ab5678901cd2", "UUID — regenerate for separate test runs"),
        var("contract_id",        "f4a5b6c7-d8e9-4123-8a45-bc6789012de3", "Assigned by Provider NP at on_select"),
        var("payment_ref",        "NEFT-20260520-093200-AXIS-045",        "NEFT transaction reference"),
        var("subject_mobile_masked", "XXXXXXX2217",      "Masked mobile for display only"),
    ]

    folders = [
        folder("01 — discover",
               "Requesting NP (ZapCharge) discovers skill certificate verification services.",
               [req("discover", "{{base_url}}/discover", discover_body,
                    "**discover** — Requesting NP → Gateway\n\n"
                    "ZapCharge Fleet Services filters for SKILL_CERTIFICATE verification with "
                    "textSearch 'NSDC EV technology certificate'. schemaContext included (catalog phase).")]),
        folder("02 — on_discover",
               "Provider NP (CertVerify India) returns its skill certificate verification catalog.",
               [req("on_discover", "{{requesting_np_uri}}/on_discover", on_discover_body,
                    "**on_discover** — Provider NP → Requesting NP\n\n"
                    "CertVerify India returns catalog. Requesting NP selects "
                    "`offer-vs-skill-hybrid-001` (₹350/request, P1D HYBRID turnaround).")]),
        folder("03 — select",
               "Requesting NP originates DRAFT contract for skill certificate verification.",
               [req("select", "{{base_url}}/select", select_body,
                    "**select** — Requesting NP → Provider NP\n\n"
                    "DRAFT Contract with skill certificate commitment (1 verification). "
                    "Minimal participant — subject and certificate details follow at init.")]),
        folder("04 — on_select",
               "Provider NP assigns contract id and returns PENDING pricing.",
               [req("on_select", "{{requesting_np_uri}}/on_select", on_select_body,
                    "**on_select** — Provider NP → Requesting NP\n\n"
                    "Provider NP assigns `{{contract_id}}`. PENDING consideration ₹350.")]),
        folder("05 — init",
               "Requesting NP submits subject reference, certificate input, purpose, and OTP consent.",
               [req("init", "{{base_url}}/init", init_body,
                    "**init** — Requesting NP → Provider NP\n\n"
                    "Requesting NP introduces: subject (Arjun Mehta), certificate input "
                    "(NSDC-EV-2024-78901, ASDC issuing body), purpose (PLATFORM_ONBOARDING), "
                    "and OTP consent reference. certificateInput is added to contractAttributes "
                    "to carry the specific certificate details to the Provider NP.")]),
        folder("06 — on_init",
               "Provider NP returns QUOTED consideration.",
               [req("on_init", "{{requesting_np_uri}}/on_init", on_init_body,
                    "**on_init** — Provider NP → Requesting NP\n\n"
                    "QUOTED consideration (₹350 NEFT UPFRONT). Payment instructions out-of-band.")]),
        folder("07 — confirm",
               "Requesting NP confirms the contract with NEFT payment authorisation.",
               [req("confirm", "{{base_url}}/confirm", confirm_body,
                    "**confirm** — Requesting NP → Provider NP\n\n"
                    "ACTIVE consideration with Axis Bank NEFT authorisation (₹350). "
                    "Provider NP begins hybrid verification (Skill India portal + manual review).")]),
        folder("08 — on_confirm  ★ Verification Started",
               "Provider NP confirms payment and indicates hybrid verification is in progress.",
               [req("on_confirm", "{{requesting_np_uri}}/on_confirm", on_confirm_body,
                    "**on_confirm** — Provider NP → Requesting NP\n\n"
                    "Contract ACTIVE. Payment received. aggregateResult INCONCLUSIVE — "
                    "hybrid verification in progress (P1D SLA). Skill India portal queried; "
                    "manual review queued. Requesting NP should poll after 1 business day.")]),
        folder("09 — status",
               "Requesting NP polls for verification result after 1 business day.",
               [req("status", "{{base_url}}/status", status_body,
                    "**status** — Requesting NP → Provider NP\n\n"
                    "Poll for hybrid verification result. Timestamp is next business day "
                    "(2026-05-21 10:00 IST). Per core spec, message.contract with id and "
                    "commitment refs (not flat contractId).")]),
        folder("10 — on_status  ★ Verification Complete",
               "Provider NP returns VERIFIED result with manual review evidence and signed PDF.",
               [req("on_status", "{{requesting_np_uri}}/on_status", on_status_body,
                    "**on_status** — Provider NP → Requesting NP\n\n"
                    "aggregateResult VERIFIED. NSDC-EV-2024-78901 confirmed — EV Technology "
                    "QP:ASC/Q1412 Level 4, ASDC issuing body, valid until 2027-09-14. "
                    "Performance includes both SOURCE_RESPONSE_HASH (automated) and "
                    "MANUAL_REVIEW_NOTES (human review). issuedCredentials carries a signed "
                    "PDF certificate valid for 6 months.")]),
    ]

    return col("VS — UC4: EV Fleet Tech Skill Certificate Verification", desc, variables, folders)


# =============================================================================
# ENVIRONMENT FILE
# =============================================================================

def build_environment():
    return {
        "id":   "f5a6b7c8-d9e0-4a12-8f56-ab7890123cde",
        "name": "Verification Service Network",
        "_postman_variable_scope": "environment",
        "values": [
            # ── Endpoints (blank — set per environment) ──────────────────────
            {"key": "base_url",          "value": "", "enabled": True,
             "description": "Provider NP (BPP) endpoint. Set to BPP sandbox / staging / integration URL."},
            {"key": "requesting_np_uri", "value": "", "enabled": True,
             "description": "Requesting NP (BAP) callback URI. Set to BAP sandbox endpoint."},
            {"key": "provider_np_uri",   "value": "", "enabled": True,
             "description": "Provider NP (BPP) URI. Used for on_* callback simulations."},
            {"key": "registry_url",      "value": "", "enabled": True,
             "description": "Network registry / CDS URL for catalog/publish."},

            # ── Auth ──────────────────────────────────────────────────────────
            {"key": "auth_token", "value": "", "enabled": True,
             "description": "Network-issued JWT — obtain from network registry before running."},

            # ── Network ───────────────────────────────────────────────────────
            {"key": "domain",     "value": "vs:verification",    "enabled": True,
             "description": "Domain prefix — confirm exact value with network team before going live."},
            {"key": "network_id", "value": "vs.in/verification", "enabled": True,
             "description": "Network ID — confirm exact value with registry team. Format: namespace/registry."},

            # ── NP identifiers ────────────────────────────────────────────────
            {"key": "requesting_np_id", "value": "requesting-np.example.in", "enabled": True,
             "description": "Requesting NP network identifier (appears as bapId in Beckn context)."},
            {"key": "provider_np_id",   "value": "provider-np.example.in",   "enabled": True,
             "description": "Provider NP network identifier (appears as bppId in Beckn context)."},

            # ── UC1 — Bus Operator DL Verification ────────────────────────────
            {"key": "transaction_id", "value": "c3d4e5f6-a7b8-4012-8d34-ef5678901aba", "enabled": True,
             "description": "UC1 transaction UUID — regenerate for each test run."},
            {"key": "contract_id",    "value": "d4e5f6a7-b8c9-4123-8e45-fa6789012bcb", "enabled": True,
             "description": "UC1 contract UUID — assigned by Provider NP at on_select."},
            {"key": "payment_ref",    "value": "UPI-20260512-103000-HDFC-001",          "enabled": True,
             "description": "UC1 UPI payment transaction reference."},

            # ── UC2 — EV Fleet Driver KYC ─────────────────────────────────────
            # (Override transaction_id / contract_id / payment_ref for UC2 runs)

            # ── UC4 — EV Tech Cert Verification ──────────────────────────────
            # (Override transaction_id / contract_id / payment_ref for UC4 runs)
        ],
    }


# =============================================================================
# VALIDATION
# =============================================================================

import re
UUID_RE = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')

def validate_collection(col_data, name):
    errors = []

    def all_items(c):
        for f in c.get("item", []):
            for item in f.get("item", []):
                yield item

    for item in all_items(col_data):
        raw  = item["request"]["body"]["raw"]
        body = json.loads(raw)
        cx   = body.get("context", {})
        action = cx.get("action", "")

        if cx.get("version") != "2.0.0":
            errors.append(f"{item['name']}: wrong version {cx.get('version')!r}")

        if '"beckn:' in raw:
            errors.append(f"{item['name']}: beckn: prefix found")

        if action not in ("discover", "on_discover", "catalog/publish", "catalog/on_publish") \
                and "schemaContext" in cx:
            errors.append(f"{item['name']}: schemaContext in non-catalog message")

        if action == "select":
            msg = body.get("message", {})
            if "contract" not in msg:
                errors.append(f"select: missing message.contract")
            if "selectedOffer" in msg:
                errors.append(f"select: stale selectedOffer found")

        mid = cx.get("messageId", "")
        if mid and not UUID_RE.match(mid):
            errors.append(f"{item['name']}: messageId not UUID: {mid!r}")

        if "networkId" not in cx and action not in ("catalog/on_publish",):
            errors.append(f"{item['name']}: networkId missing")

        if action in ("select", "init", "confirm", "on_status"):
            contract = body.get("message", {}).get("contract", {})
            for i, cm in enumerate(contract.get("commitments", [])):
                offer = cm.get("offer", {})
                if "resourceIds" not in offer:
                    errors.append(f"{item['name']}: commitment[{i}].offer missing resourceIds")

        if action == "status":
            msg = body.get("message", {})
            if "contractId" in msg:
                errors.append(f"status: flat contractId — use message.contract.id")

        contract = body.get("message", {}).get("contract", {})
        for banned in ("billingDetails", "paymentInstructions", "invoiceDetails"):
            if banned in contract:
                errors.append(f"{item['name']}: contract.{banned} not valid")

    if errors:
        print(f"\n  VALIDATION ERRORS in {name}:")
        for e in errors:
            print(f"    ✗ {e}")
        return False
    return True


# =============================================================================
# MAIN
# =============================================================================

collections = [
    ("VS_Catalog_Publish_Collection.json",                build_catalog_publish()),
    ("VS_UC1_BusOperator_DL_Verification_Collection.json", build_uc1()),
    ("VS_UC2_EVFleet_DriverKYC_Collection.json",           build_uc2()),
    ("VS_UC4_EVFleet_TechCert_Verification_Collection.json", build_uc4()),
]

all_ok = True
for filename, col_data in collections:
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(col_data, f, indent=2, ensure_ascii=False)
    ok = validate_collection(col_data, filename)
    if not ok:
        all_ok = False
    folders = len(col_data.get("item", []))
    requests = sum(len(f.get("item", [])) for f in col_data.get("item", []))
    variables = len(col_data.get("variable", []))
    status_str = "✓" if ok else "✗"
    print(f"{status_str} Written: {filename}  ({folders} folders, {requests} requests, {variables} variables)")

# Environment file
env_path = os.path.join(OUTPUT_DIR, "VS_Environment.json")
with open(env_path, "w", encoding="utf-8") as f:
    json.dump(build_environment(), f, indent=2, ensure_ascii=False)
print(f"✓ Written: VS_Environment.json")

print(f"\n{'All collections passed validation.' if all_ok else 'Some collections have validation errors — see above.'}")
print(f"Output directory: {OUTPUT_DIR}")
