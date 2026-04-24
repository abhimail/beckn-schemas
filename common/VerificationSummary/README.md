# VerificationSummary

**Container:** inline sub-schema (shared utility type)
**Tag:** common shared-type hiring skilling

Summary of credential verification outcome. Carries the result of a verification check (status, verifying agency, timestamp) without embedding the VC payload itself — keeps contract messages lightweight while providing enough signal for workflow automation.

Used by:
- `JobApplicationContract.prerequisite_verification_summary` — pre-hiring credential checks
- `JobApplicationPerformance.verification_summary` — verification during evaluation steps
- `hiring-candidates/EmployerHiringContract` — employer-side verification tracking
- `hiring-candidates/HiringProcessPerformance` — verification during hiring process
- `skilling/CourseEnrollmentContract` — course entry credential verification
