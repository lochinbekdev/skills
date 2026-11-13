# Contributing

## The shape of a change

These skills are deliberately narrow. The reason to add one is that an area is uncovered, not
that an existing skill is long. The reason to change one is that it behaved wrongly in a real
run — so say which agent, which target, and what it did.

Before opening a pull request:

```bash
python3 scripts/validate-repo.py
```

It checks that every skill's frontmatter name matches its directory and the agent-skills name
rules, that each `agents/openai.yaml` stays inside the documented 25-64 character
`short_description` and names its own skill in `default_prompt`, that both plugin manifests
agree on a strict-semver version, and that every bundled `references/` copy is identical to
its source under `docs/`. CI runs the same script.

## Where things live

- `docs/` is the **only** source for the six shared standards. Edit there, then run
  `./scripts/sync-docs.sh` and commit the refreshed copies under
  `skills/security/*/references/`. Editing a copy directly is the one change CI will reject
  outright.
- `docs/harness-notes.md` is repo-facing and deliberately not bundled: it records what differs
  between agents, from real runs, with raw transcripts left out.
- `.agents/install-block.md` is the canonical install wording. Change it there first, then
  propagate to `README.md`.
- A skill's own rules live in its `SKILL.md`. Keep the five invariants near the top: a sandbox
  can block `references/`, and a skill that loses them stops being safe.

## Naming

A skill's `name` must equal its directory name, and may only contain lowercase letters, digits
and single hyphens (1-64 characters). Do not prefix it with the vendor: both Claude Code and
Codex namespace plugin-bundled skills by the plugin, so a prefix shows the publisher twice.

## Releasing

Bump `version` in `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json` together,
add a `CHANGELOG.md` entry, then tag:

```bash
claude plugin tag .
git push --tags
```

An installed plugin only picks up a change when the version changes, so a fix that ships to
users needs a bump even when the diff is small.
