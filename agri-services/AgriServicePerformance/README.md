# AgriServicePerformance Schema

**Container:** `Performance.performanceAttributes`
**Protocol Version:** 2.0
**Semantic Model:** generalised
**Use Cases:** Agricultural service delivery tracking, livestock vaccination records, farm visit documentation
**Tags:** agri-services-ext, agriculture, livestock

## Overview

AgriServicePerformance extends ServicePerformance with agriculture-specific fields for tracking livestock service delivery at farms.

## Extension Details

Extends: ServicePerformance (../../../generic-service/ServicePerformance/v2.1/attributes.yaml)

Additional fields:
- farmLocation: Hierarchical location (village, ward, county, country, GPS, landmark)
- livestockCount: Number of animals serviced
- livestockType: Type of livestock (poultry, cattle, goat, sheep, pig, other)

## Design Rationale

Agricultural services are inherently tied to specific farms and livestock. This schema adds those specifics while maintaining all the generic performance tracking fields (appointment time, completion status, follow-up scheduling).

## Use Cases

- Vaccination visit documentation
- Poultry flock inspection records
- Feed/input delivery to farms
- Disease screening records
- Training delivery at farm sites
