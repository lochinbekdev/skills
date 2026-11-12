---
name: dependency-supply-chain
description: Audit a backend's dependencies, lockfiles, runtime/framework versions, CI/CD build pipeline, and secret exposure for supply-chain risk — read-only, no installs or auto-fixers. Use when the user wants a dependency/SCA/supply-chain or CI/CD security review, or runs /dependency-supply-chain.
---

# Dependency & supply-chain audit

Focused, **read-only** skill. Read first: `docs/write-boundary.md`, `docs/report-standard.md`.

## Hard constraint
**Never install or update packages, run auto-fixers, or run `npm audit fix` / dependency
install/update.** Inspect manifests, lockfiles, and advisories; do not execute project code.

## Checks
- **Dependencies** — direct and transitive deps with lock references; known-vulnerable versions
  cross-checked against advisories as of the audit date. A manifest constraint or image tag is
  **not** proof of the actual deployed patch version — mark version unknowns explicitly.
- **Runtime/framework & native versions** — exact language/runtime and framework patch levels;
  correspondence with the installed/deployed build.
- **CI/CD & build supply chain** — pipeline definitions, build steps, third-party actions/images,
  pinning, artifact integrity, and privilege of build credentials.
- **Secrets & configuration** — hardcoded credentials, tokens, keys in code/config/CI/history;
  report class and location without exfiltrating the secret value.
- **Forgotten features, package routes, and CLIs** exposed by dependencies.

## Rules
- Distinguish a declared constraint from the real runtime version; state the limitation when the
  deployed version cannot be confirmed.
- Threat intel must be dated; label results `confirmed` / `partial` / `blocked` / `not-tested`.
- No writes beyond the single report. No network calls that execute project code.

Fold all results and evidence into the single report (`docs/report-standard.md`), written in **English by default** (or the user's chosen language).
