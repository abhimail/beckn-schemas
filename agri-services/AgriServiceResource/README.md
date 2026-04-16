# AgriServiceResource Schema

**Container:** `Resource.resourceAttributes`
**Protocol Version:** 2.0
**Semantic Model:** generalised
**Use Cases:** Agricultural service discovery, poultry/livestock services, agricultural extension services
**Tags:** agri-services-ext, agriculture, livestock

## Overview

AgriServiceResource extends ServiceResource with agriculture-specific fields for representing livestock and farm-related services.

## Extension Details

Extends: ServiceResource (../../../generic-service/ServiceResource/v2.1/attributes.yaml)

Additional fields:
- serviceCategory: VACCINATION, BROODING, INCUBATION, AGRI_INPUT, ADVISORY, SCREENING
- providerType: VET, AGROVET, EXTENSION_OFFICER, AGRI_INPUT_DEALER, AGRI_TRAINER
- livestockTypes: POULTRY, CATTLE, GOAT, SHEEP, PIG, OTHER
- serviceAreaHierarchy: village, ward, county, country, coverageRadiusKm

## Design Rationale

Agriculture services require specific livestock types, service categories, and hierarchical geographic organization (village/ward/county). These are additive to the base ServiceResource without changing its core semantics.

## Use Cases

- Veterinary consultation services
- Poultry vaccination campaigns
- Agricultural input supply
- Extension officer advisory services
- Farmer training programs
