# DriverCandidateProfileResource

**Container:** `beckn:resourceAttributes`  
**Use Cases:** UC2 — Operator Initiated Driver Recruitment  
**Tag:** transport-hiring

Extension attributes for a driver candidate profile Resource. Published by
driver platforms and aggregators. Extends CandidateProfileResource with
driver-specific role types, vehicle categories, home location, reputation
summary, and credential summary.

Category discriminator: `driver-candidate`  
Privacy: passport_reference is stage-gated (init+ only). Home location GPS
must be locality-level only at discovery.
