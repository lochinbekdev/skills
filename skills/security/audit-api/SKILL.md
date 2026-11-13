---
name: audit-api
description: Audit a backend's web/API surface with matched control/test requests. Use for API endpoint review, OWASP Top 10, injection, SSRF, CORS or header checks.
---

# API surface audit

Focused skill for the externally reachable web/API surface. Read first:
`references/intake.md`, `references/test-accounts.md`, `references/write-boundary.md`, `references/report-standard.md`, `references/tooling.md` (SAST/DAST breadth via existing safe scanners), `references/findings-quality.md` (confidence & export).

## Non-negotiable invariants

Some harnesses cannot read a file outside the working directory, so a sandbox may block the
`references/` files above. They are the full rules; these five hold even when you cannot open
them, and you state in the report which references you could not read:

1. **Authorized scope only.** A host, domain, IP or credential found in the repo does not
   authorize testing it. Live requests and mutations need an explicit "boshla"/"go".
2. **Read-only.** The audit writes exactly one file, the report. No fixes, no installs, no
   migrations, no seeds, no auto-fixers. Record `git status` before and after.
3. **Evidence or nothing.** `HTTP 200` is not proof. Every claim carries a `path:line` or a
   matched control/test request pair; every mutation gets a separate read and a verified
   rollback; every finding carries `confirmed` / `likely` / `unconfirmed`.
4. **Inventory is not the deliverable.** Summarise with counts, cap any inventory table at 30
   rows, and never paste file trees, directory listings or raw tool output as a section.
5. **Incomplete means `PARTIAL AUDIT`.** If a required test did not run, say so in the title
   and the summary with the blocker, and never claim the system is secure.

## How this skill starts
Follow `references/intake.md`: inventory routes and input handling yourself read-only, then ask
the user — one round of numbered `Q1/Q2…` questions with recommended answers — only the
gaps (authorized test env/base URL, in/out-of-scope endpoints, accounts, rate limit).
Explain which endpoints and checks will run, then send real requests **only after an
explicit "boshla"/"go".** Static review may proceed before that.

## Inventory
Routes are not always in the route files: many frameworks register them via attributes or
annotations (e.g. `spatie/laravel-route-attributes`, Symfony/Spring annotations, NestJS
decorators), so `routes/*.php` can be nearly empty while controllers hold the real surface —
scan controllers too. When a server is available, confirm reachability with read-only
introspection (`php artisan route:list`, `rails routes`) per `references/write-boundary.md`.

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
- Use matched control/test pairs (`references/test-accounts.md`): establish a legitimate request, then
  change only the tested factor.
- A failed legitimate control leaves the comparison inconclusive — diagnose endpoint/login/object
  first. A malformed-body `400/422` or wrong URL does not establish correct authorization.
- `HTTP 200` alone is not proof — inspect the body. Keep horizontal/vertical/tenant results distinct
  (delegate deep authz cases to `audit-access-control`).
- Read-only boundary applies: no fixtures, scripts, or artifacts on disk. No DoS, brute force, or
  broad enumeration. No RCE, deserialization gadgets, or active webshells.

Fold all results and evidence into the single report (`references/report-standard.md`), written in **English by default** (or the user's chosen language).
