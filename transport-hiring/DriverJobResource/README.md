# DriverJobResource

**Container:** `beckn:resourceAttributes`  
**Use Cases:** UC1 — Driver/Aggregator Initiated Job Application  
**Tag:** transport-hiring

Extension attributes for a driver job vacancy Resource published by an
operator platform. Extends the generic `HiringJobResource` with driver-specific
fields: role type, vehicle categories, shift pattern, required credentials,
training requirements, and operator reputation.

Category discriminator: `driver-job`  
Privacy: `application_instructions` is stage-gated (on_select only).
