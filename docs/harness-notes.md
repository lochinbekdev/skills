# Harness notes

What differs between agents when these skills run, and what the skills do about it. Every
entry comes from a run against a real Laravel 12 backend, not from reading documentation.
Keep raw transcripts out of this file: they carry hostnames, endpoints and account data.

## Baseline runs (2026-11-13)

Four headless runs, same target, same two prompts — one bare ("audit this backend for security
issues"), one with scope, accounts and limits supplied up front. Codex: `codex exec -s
read-only`, codex-cli 0.167.0, `gpt-5.4`. Claude Code: `claude -p`, Write/Edit disabled.

| Run | Output | Behaviour |
|---|---|---|
| Codex, bare | 17 lines | `PARTIAL AUDIT`, 6 findings with `path:line` evidence, blocked live testing pending "go" |
| Codex, scoped | 94 lines | Structured report, inventory summarised in tables, 1 high / 2 medium, 0 runtime-confirmed |
| Claude Code, bare | 33 lines | Stopped at intake with Q1-Q7, 7 preliminary findings |
| Claude Code, scoped | 276 lines | Fullest report: 3 high (2 confirmed by unauthenticated live GET), 5 medium, 5 low |

No run produced a file-listing dump, so the originally reported symptom did not reproduce under
these conditions. Three other defects did, and all three are fixed:

## Codex does not delegate unless asked explicitly

Codex read the orchestrator and then did the whole audit itself, never reaching the five
focused skills — 3-6 findings against Claude Code's 13 on the same target. Codex delegates
when a skill's instructions request it; "delegate the focused work" in passing is not a
request. Step 5 of the orchestrator now asks for one agent per companion skill, in parallel,
and states the inline fallback for harnesses without sub-agents.

## A sandbox can block `references/`

Claude Code, loading a skill through a symlink outside its working directory, could not open a
single bundled reference and said so in its first line. Bundling the shared docs inside each
skill is necessary but not sufficient: the five invariants are now restated in every
`SKILL.md`, and a report must name the references it could not read.

## `codex exec -s read-only` has no network

Every HTTP attempt returns `Operation not permitted`, including to `localhost`. The skill
handled it correctly (reported zero executed workflows, marked `PARTIAL AUDIT`), but live
testing under Codex needs `-s workspace-write` or an interactive session. The install block
says so.

## Invocation differs

Claude Code exposes a per-skill slash command, namespaced by plugin:
`/lochinbekdev-security:audit-backend`. Codex has no per-skill slash command; it uses `$name`
or the `/skills` picker.

**Codex namespaces plugin-bundled skills too**, as `$<plugin>:<skill>` —
`$lochinbekdev-security:audit-api`. This is not in OpenAI's public docs, and the opposite was
inferred here on 2026-11-13 from the shipped first-party plugins, whose skill `name` fields
carry hand-written prefixes (`figma-spec`, `figma-use`). That inference was wrong: observing
the real picker showed the plugin prefix already applied. The skills briefly shipped as
`lochinbekdev-audit-*` and appeared as `$lochinbekdev-security:lochinbekdev-audit-api`, so the
names went back to bare `audit-*`.

Consequence: the vendor prefix belongs to the plugin, not the skill name. Installed outside a
plugin — the `scripts/link-skills.sh` symlink route — a skill is reached by its bare name
(`$audit-api`, `/audit-api`), since there is no plugin to namespace it.
