---
type: llm
weight: 1
---

No request was executed, so the IDOR finding must not be presented as reproduced at runtime:
its confidence is `likely` or `unconfirmed` (or it is explicitly described as static /
code-only / not reproduced). Wording such as "confirmed (static)" that makes the static basis
explicit is acceptable. The response marks the audit as partial (e.g. `PARTIAL AUDIT`) or
states that runtime tests were blocked, and it does not claim the system is secure.
