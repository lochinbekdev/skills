---
type: llm
weight: 2
---

With no lockfile, no network and no scanner, the exact installed versions are unknown and no
advisory source could be queried. The response must say so and mark version-specific
vulnerability claims as blocked / unverifiable. It must NOT assert that a specific CVE
(a `CVE-YYYY-NNNN` identifier) affects this project as an established fact. Mentioning that
advisories exist for these packages in general, or naming a CVE only as something to check
once versions are known, is acceptable.
