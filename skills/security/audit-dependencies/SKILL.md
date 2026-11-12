---
name: audit-dependencies
description: Audit a backend's dependencies, lockfiles, runtime/framework versions, CI/CD build pipeline, and secret exposure for supply-chain risk — read-only, no installs or auto-fixers. Use when the user wants a dependency/SCA/supply-chain or CI/CD security review, or runs /audit-dependencies.
---

# Dependency & supply-chain audit

Focused, **read-only** skill. Read first: `references/write-boundary.md`, `references/report-standard.md`,
`references/tooling.md` (safe scanners + live CVE data), `references/findings-quality.md` (confidence & export).

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
read-only to stdout — `osv-scanner`, `trivy fs`, `npm/pnpm/pip/cargo/composer audit --json`,
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
