# The canonical install block

One install story, one wording. `README.md` and anything under `docs/` must say **this** and
nothing else. Change it here first, then propagate.

## Rules

- Lead with routes that update themselves. Label every other route "manual updates".
- Name the invocation syntax beside each install command: a user who installed the plugin and
  cannot call it has not finished installing.
- State a route's known limits where the user will hit them, not in a footnote.
- Claim nothing unverified. Each block below records when it was last run, and against what.

| Agent | Route | Updates itself? |
|---|---|---|
| Claude Code | `lochinbekdev` marketplace (`.claude-plugin/`) | Yes, by default |
| Codex | `lochinbekdev` marketplace (`.codex-plugin/`) | Yes, at startup |
| Any other agent | `scripts/link-skills.sh` symlinks | No. Run `git pull` |

Other agents (Copilot, Gemini, Cursor, …) are deliberately absent: nobody has run this repo
against them. Add a row only after running one, with the date.

## Claude Code

<canonical-block name="claude-code">

```bash
/plugin marketplace add lochinbekdev/skills
/plugin install lochinbekdev-security@lochinbekdev
```

Updates itself by default. The five focused skills are model-invoked — "audit the uploads in
this project" reaches them. The orchestrator is user-invoked, so name it:

```bash
/lochinbekdev-security:audit-backend
```

</canonical-block>

Verified 2026-11-13: plugin loads, skills resolve under their new names.

## Codex

<canonical-block name="codex">

```bash
codex plugin marketplace add lochinbekdev/skills
codex plugin add lochinbekdev-security@lochinbekdev
```

Updates itself at startup. **Restart Codex after installing**, or the new skills stay
undiscovered. Codex has no per-skill slash command, and it namespaces plugin-bundled skills by
the plugin, so invoke with `$lochinbekdev-security:audit-backend` or run `/skills` to browse. Live HTTP testing needs a sandbox that permits network: under
`codex exec -s read-only` every request fails with `Operation not permitted`, and the audit
correctly reports zero executed workflows.

</canonical-block>

Unverified against a published marketplace: the manifest exists in this repo, but the install
pair above has not been run end to end (it needs the manifest on the default branch upstream).
Say so until someone runs it.

## Any other agent, or a local checkout

<canonical-block name="link-script">

```bash
git clone https://github.com/lochinbekdev/skills
cd skills
./scripts/link-skills.sh
```

Symlinks every skill into `~/.agents/skills` (Codex and other generic agents) and
`~/.claude/skills` (Claude Code outside the plugin), then prunes links it made earlier that now
dangle. `git pull` updates the skills in place; restart the agent to pick up new ones.

</canonical-block>

Verified 2026-11-13: Codex discovered all six skills through these symlinks and read their
bundled `references/`. Claude Code, loading the same symlinks, was denied the reference files
by its sandbox and ran on the `SKILL.md` body alone — which is why the invariants are restated
there.
