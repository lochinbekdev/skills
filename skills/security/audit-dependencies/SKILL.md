---
name: audit-dependencies
description: Audit dependencies, lockfiles, runtime and framework versions, CI/CD pipelines and secret exposure. Use for dependency, SCA, supply-chain or CI/CD security review. Read-only; no installs or auto-fixers.
---

# Dependency & supply-chain audit

Focused, **read-only** skill. Read first: `references/write-boundary.md`, `references/report-standard.md`,
`references/tooling.md` (safe scanners + live CVE data), `references/findings-quality.md` (confidence & export).

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
This skill needs **no live access or test accounts**, so it does **not** run the full intake
interview (`references/intake.md`). It runs directly on the repo already in scope: read manifests,
lockfiles, CI, and config read-only and produce findings. Ask the user only if the repo path
or audit scope is genuinely ambiguous; otherwise proceed and mark any unconfirmable item
(e.g. the deployed runtime patch version) as `blocked`.

## Hard constraint
**Never install or update packages, run auto-fixers, or run `npm audit fix` / dependency
install/update.** Inspect manifests, lockfiles, and advisories; do not execute project code.

## Tooling first (breadth + fresh data)
Per `references/tooling.md`, widen coverage with tools that are **already installed** and run
read-only to stdout — `osv-scanner`, `trivy fs`, `npm/pnpm/pip/cargo audit --json`,
`composer audit --locked --format=json` (**always `--locked`** on a read-only checkout — a
plain `composer audit` prints "No packages" and exits 0, a silent false-clean),
`govulncheck`, plus `gitleaks`/`trufflehog` for secrets. **Never install or auto-fix.** For
per-dependency CVEs, query a **live advisory source** (OSV `api.osv.dev/v1/query`) rather than
model memory; if no scanner and no network, mark version-specific CVE claims `blocked`.

## Checks
- **Dependencies** — direct and transitive deps with lock references; cross-check versions
  against **live** advisories (OSV/vendor), not memory. A manifest constraint or image tag is
  **not** proof of the actual deployed patch version — mark version unknowns explicitly.
- **Runtime/framework & native versions** — exact language/runtime and framework patch levels;
  correspondence with the installed/deployed build.
- **CI/CD & build supply chain** — pipeline definitions, build steps, third-party actions/images,
  pinning, artifact integrity, and privilege of build credentials.
- **Secrets & configuration** — hardcoded credentials, tokens, keys in code/config/CI/history;
  use entropy/pattern scanning for breadth, then confirm. Report class and location **without
  exfiltrating the secret value**.
- **Forgotten features, package routes, and CLIs** exposed by dependencies.

## Rules
- Treat scanner output as **leads**: confirm each relevant hit, assign a confidence and stable
  ID, and challenge false positives (`references/findings-quality.md`).
- Distinguish a declared constraint from the real runtime version; state the limitation when the
  deployed version cannot be confirmed.
- Threat intel must be **dated and sourced** (cite the advisory/tool + version).
- No writes beyond the report (plus the agreed SARIF/JSON export). No calls that execute project code.

Fold all results and evidence into the single report (`references/report-standard.md`), written in **English by default** (or the user's chosen language).
