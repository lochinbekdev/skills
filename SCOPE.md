# Scope

This marketplace currently ships **security** skills only. Every skill is:

- **Read-only by default** — an audit never changes the inspected project; the only written
  file is the security report (default `SECURITY_AUDIT_REPORT.md`; see `docs/write-boundary.md`).
- **Evidence-based** — real HTTP tests with the agreed test accounts, matched control/test
  pairs, and a separate read after every mutation (see `docs/test-accounts.md`).
- **Standardized** — one report structure, written in **English by default** (user-selectable), with a `PARTIAL AUDIT`
  marker rule (see `docs/report-standard.md`).

## In scope
Authorized backend security audits: authorization/IDOR/tenant isolation, API surface,
upload/storage pipeline, and dependency/supply-chain review.

## Out of scope
Applying fixes, DoS/brute force/enumeration, RCE/webshells, pivoting to third-party or
production targets, and any destructive or irreversible action. These require separate
authorization and are not performed by these skills.
