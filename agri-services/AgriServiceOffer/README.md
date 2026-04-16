# AgriServiceOffer Schema

**Container:** `Offer.offerAttributes`
**Protocol Version:** 2.0
**Semantic Model:** generalised
**Use Cases:** Agricultural input supply offers, crop variety specification
**Tags:** agri-services-ext, agriculture

## Overview

AgriServiceOffer extends ServiceOffer with agriculture-specific fields for specifying agricultural inputs and crop varieties.

## Extension Details

Extends: ServiceOffer (../../../generic-service/ServiceOffer/v2.1/attributes.yaml)

Additional fields:
- inputBrandOrVariety: Brand name or crop variety for agricultural input services

## Design Rationale

Agricultural input services need to specify what brand or variety is being offered. This is a single additive field to the base ServiceOffer.

## Use Cases

- Certified seed supply (e.g., "KCOOP-DH02" variety maize)
- Fertilizer brand supply
- Feed supply offers
- Pesticide/herbicide supply
