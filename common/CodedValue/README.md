# CodedValue

**Container:** inline sub-schema (shared utility type)
**Tag:** common shared-type

A classification code governed by an external authority (e.g. ISIC industry codes, NSQF qualification levels, HS commodity codes). Carries the authority URI alongside the code so consumers can resolve it against the correct registry without ambiguity.

Used by:
- `HiringJobResource.industry_type` — ISIC industry classification
- `CandidateProfileResource.qualification_level` — NSQF or equivalent qualification level
- `CandidateProfileResource.industry_preference` — preferred industries
- `skilling/CourseResource` — course classification
