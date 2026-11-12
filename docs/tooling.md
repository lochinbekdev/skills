# Augmenting manual review with tools & live data (shared)

Scanners beat a human on breadth, speed, and fresh vulnerability data; manual review beats
them on business logic and authorization. These skills combine both **without breaking the
read-only write boundary** (`write-boundary.md`).

## Live vulnerability data is the PRIMARY path (do not trust model memory)
Model knowledge has a cutoff, so dependency CVEs may be stale or wrong. Treat a live advisory
query as the **default**, whether or not a scanner is installed. When network access is agreed:
- **OSV (works everywhere, no install):** POST to `https://api.osv.dev/v1/query` with
  `{"package":{"name":"<pkg>","ecosystem":"<Packagist|npm|PyPI|Go|crates.io|…>"},"version":"<v>"}`,
  or `https://api.osv.dev/v1/querybatch` for many packages at once. This is the recommended
  primary method; it needs only an HTTP client.
- Vendor/distro advisories and the project's own advisory DB where applicable.
If no network is available, say so and mark version-specific CVE claims `blocked` rather than
asserting them from memory.

## Use existing safe tools when present (do not install)
If a scanner is **already installed** and can run **read-only to stdout** without executing
project code or writing files/caches, use it to widen coverage, then reason over its output:
- SAST: `semgrep --json` (read-only rules), language linters in check-only mode.
- Dependencies/SCA: `osv-scanner`, `trivy fs`/`trivy repo` on manifests/lockfiles,
  `npm/yarn/pnpm audit --json`, `pip-audit`, `govulncheck`, `cargo audit`, `composer audit`.
- Secrets: `gitleaks detect --no-banner` / `trufflehog` in read-only mode.
- Containers/IaC: `trivy config`, `checkov -o json`.

Rules:
- **Never install, update, or auto-fix** (`npm audit fix` is forbidden). Only run what exists.
- Refuse any tool that executes project code, writes caches/reports/logs, or needs a profile.
  If it cannot run read-only to stdout, mark that check **blocked** and fall back to the OSV
  HTTP queries above plus manual review — that fallback is expected, not exceptional.
- Treat tool output as **leads, not verdicts**: confirm each relevant finding manually and
  label its status and confidence per `findings-quality.md`. Record which tool/version produced it.

## Version resolution when there is no lockfile
A manifest constraint is not a deployed version. For a declared range with **no committed
lockfile**, reason about the whole resolvable range, not one number:
- If the **entire allowable range is vulnerable** (e.g. `^0.19` on a package whose fixes only
  exist at a higher major, so the range caps inside vulnerable versions) → report **confirmed
  for the range**, `blocked` for the exact deployed version.
- If a **fixed version exists within the range** (e.g. `^4.17.19` where a patched 4.17.x is in
  range) → the floor is vulnerable but the deployed build may be patched → mark **blocked**
  pending the lockfile/deployed version; recommend committing a lockfile.
- Always state which you did and request the lockfile or deployed manifest to close the gap.

## Handling secrets without exfiltrating them
When reporting a secret (hardcoded, in `.env`, or in history), **never read or print its
value.** Prove presence by non-sensitive means only: the key name, file and line, and at most
a length or a salted/truncated hash. Report class (API key, DB password, JWT secret…) and
location, plus whether it is tracked in git history. Do not paste the value anywhere, including
the report.

## When to lean on tools vs. manual
- **Tools/live data first** for breadth: dependency CVEs, secrets, known SAST patterns, misconfig.
- **Manual only** for what scanners miss: horizontal/vertical/tenant authorization, business
  logic, workflow/state abuse, chained attacks. This is the core value of these skills.
