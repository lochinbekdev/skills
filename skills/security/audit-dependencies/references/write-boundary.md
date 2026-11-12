# Write boundary (shared rule)

Every skill in this plugin is **read-only by default**. An audit must not change the
project it inspects. These rules are referenced by every security skill.

## Allowed
- Read source, configuration, manifests, lockfiles, and Git metadata (`git status`,
  `git diff`, `git log`) — read only.
- Create or update **one** deliverable: the security report (default `SECURITY_AUDIT_REPORT.md`
  at the audited project root, or an agreed path — see `report-standard.md`), plus its parent
  directories.
- Send real HTTP requests to the **agreed** test environment with the **agreed** test
  accounts, within the authorized, reversible scope (see `test-accounts.md`).

## Forbidden
- Creating, editing, moving, or deleting source, config, manifests, dependencies,
  lockfiles, migrations, `.env`, Docker/CI files, or any file other than the report.
- Separate `evidence/`, `findings/`, scripts, logs, JSON/CSV, screenshots, archives,
  or downloads — including temporary files that are deleted afterward. Keep all
  inventories, excerpts, requests/responses, and results **inside the report**.
- Installing/updating packages, running auto-fixers, formatters, builds, codegen,
  migrations, seeds, deploys, or any command that writes files (`npm audit fix`,
  dependency install/update, etc.).
- Mutating Git state: add, commit, push, checkout/switch, restore/reset, clean,
  stash, merge/rebase, pull/fetch, init, or config changes.
- Tools with side effects: cookie jars, shell history, caches, bytecode/`__pycache__`,
  profiles, auto-reports, app logs, or DB files. Keep sessions/tokens in memory only.
- Persistent browser profiles, storage-state, screenshots, videos, HAR, traces, or
  downloads. Use isolated, nonpersistent contexts or mark the check blocked.

## Baseline check
Before any write or test, record project root, time/zone, current commit, and
`git status --porcelain=v1 --untracked-files=all`. Repeat at the end and compare.
**The report must be the only file the auditor created or changed.** If unexpected
changes appear, stop side-effecting actions, document the cause, and do not auto-restore.
