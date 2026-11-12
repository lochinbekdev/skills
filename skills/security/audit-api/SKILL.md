---
name: audit-api
description: Audit the web/API surface of a backend — routes, input handling, injection, SSRF, CORS, headers, and business-logic abuse — with matched control/test requests. Use when the user wants API endpoint security review, OWASP Top 10 web testing, injection/SSRF/CORS checks, or runs /audit-api.
---

# API surface audit

Focused skill for the externally reachable web/API surface. Read first:
`docs/test-accounts.md`, `docs/write-boundary.md`, `docs/report-standard.md`.

## How this skill starts
Follow `docs/intake.md`: inventory routes and input handling yourself read-only, then ask
the user — one round of numbered `Q1/Q2…` questions with recommended answers — only the
gaps (authorized test env/base URL, in/out-of-scope endpoints, accounts, rate limit).
Explain which endpoints and checks will run, then send real requests **only after an
explicit "boshla"/"go".** Static review may proceed before that.

## Inventory
For each route record: HTTP method/path, mounting/reachability, authentication, permissions,
owner/tenant filters, input fields, and affected data. An action name inferred from conventions
is **not** proof of an externally reachable endpoint — confirm reachability.

## Checks (record a result for every item)
- **Injection** — SQL/NoSQL/command/ORM/template; trace input → parameterization → sink.
- **SSRF** — URL-import, webhooks, previews, server-side fetch; check allowlists and metadata-
  endpoint exposure. Use only agreed, inert in-scope targets; never pivot to third parties.
- **Reflected/stored XSS & response context** — mark browser-dependent claims unconfirmed unless
  verified in an isolated, nonpersistent browser context (no artifacts).
- **CORS** — origin/credential policy, reflection, null origin; prove any cross-origin access.
- **Security headers**, cookie flags, CSRF protection, content-type handling, mass assignment.
- **Business logic** — price/quantity, negative/overflow values, coupon/limit abuse, races/
  TOCTOU/transactions. Execute full workflow/state/role paths and forbidden transitions. No
  harmful or parallel load tests.

## Rules
- Use matched control/test pairs (`docs/test-accounts.md`): establish a legitimate request, then
  change only the tested factor.
- A failed legitimate control leaves the comparison inconclusive — diagnose endpoint/login/object
  first. A malformed-body `400/422` or wrong URL does not establish correct authorization.
- `HTTP 200` alone is not proof — inspect the body. Keep horizontal/vertical/tenant results distinct
  (delegate deep authz cases to `audit-access-control`).
- Read-only boundary applies: no fixtures, scripts, or artifacts on disk. No DoS, brute force, or
  broad enumeration. No RCE, deserialization gadgets, or active webshells.

Fold all results and evidence into the single report (`docs/report-standard.md`), written in **English by default** (or the user's chosen language).
