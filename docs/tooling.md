# Augmenting manual review with tools & live data (shared)

Scanners beat a human on breadth, speed, and fresh vulnerability data; manual review beats
them on business logic and authorization. These skills combine both **without breaking the
read-only write boundary** (`docs/write-boundary.md`).

## Use existing safe tools (do not install)
If a scanner is **already installed** and can run **read-only to stdout** without executing
project code or writing files/caches, use it to widen coverage, then reason over its output:
- SAST: `semgrep --json` (read-only rules), language linters in check-only mode.
- Dependencies/SCA: `osv-scanner`, `trivy fs` / `trivy repo` on manifests/lockfiles,
  `npm/yarn/pnpm audit --json`, `pip-audit`, `govulncheck`, `cargo audit`, `composer audit`.
- Secrets: `gitleaks detect --no-banner` / `trufflehog` in read-only mode.
- Containers/IaC: `trivy config`, `checkov -o json`.

Rules:
- **Never install, update, or auto-fix** (`npm audit fix` is forbidden). Only run what exists.
- Refuse any tool that executes project code, writes caches/reports/logs, or needs a profile.
  If it cannot run read-only to stdout, mark that check **blocked** and fall back to manual.
- Treat tool output as **leads, not verdicts**: confirm each relevant finding manually and
  label its status per `docs/findings-quality.md`. Record which tool/version produced it.

## Live vulnerability data (do not trust model memory)
Model knowledge has a cutoff, so dependency CVEs may be stale. When network access is agreed,
query an authoritative source read-only and cite it, instead of recalling from memory:
- OSV: `https://api.osv.dev/v1/query` (POST package+version) for per-dependency advisories.
- Vendor/distro advisories and the project's own advisory DB where applicable.
If no network is available, say so and mark version-specific CVE claims as `blocked` rather
than asserting them from memory.

## When to lean on tools vs. manual
- **Tools first** for breadth: dependency CVEs, secrets, known SAST patterns, misconfig.
- **Manual only** for what scanners miss: horizontal/vertical/tenant authorization, business
  logic, workflow/state abuse, chained attacks. This is the core value of these skills.
