# CredentialRequirement

**Container:** inline sub-schema (shared utility type)
**Tag:** common shared-type hiring

A prerequisite credential or certification that a candidate must hold or a learner must have completed. Describes the requirement (type, issuing authority, minimum level) without carrying the credential document itself — documents are referenced at the Contract stage via SubmittedDocument.

Used by:
- `HiringJobResource.requirements` — credential prerequisites for a job vacancy
- `skilling/CourseResource` — entry requirements for a course
