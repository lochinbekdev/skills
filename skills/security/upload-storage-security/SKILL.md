---
name: upload-storage-security
description: Audit the upload → storage → processing → serving pipeline of a backend — file-type/path handling, archive extraction (zip-slip), SSRF on URL import, EXIF/CSV-formula injection, and download authorization. Use when the user wants file-upload security review or runs /upload-storage-security.
---

# Upload / storage / processing / serving security

Focused skill for the file pipeline. Read first: `docs/write-boundary.md`,
`docs/test-accounts.md`, `docs/report-standard.md`.

## How this skill starts
Follow `docs/intake.md`: locate the upload/storage/serving endpoints yourself read-only,
then ask the user — one round of numbered `Q1/Q2…` questions with recommended answers —
only the gaps (authorized test env, upload/download endpoints, accounts A/B, agreed small
inert test inputs, authorized reversible actions). Explain the pipeline tests, then upload
or mutate **only after an explicit "boshla"/"go".** Static review may proceed before that.

## Checks
- **Type & name handling** — content-type vs real content, extension/MIME confusion, dangerous
  filenames, path traversal in stored path, overwrite containment.
- **Archive extraction** — zip-slip, nested/symlink entries, path/overwrite containment, and
  expanded-size/ratio/count limits. ZIP creation does **not** prove extraction exists. **Do not
  create or execute decompression bombs.**
- **Post-upload serving** — rendering/serving of internal executable/HTML/SVG files, content
  disposition, and the origin files are served from.
- **URL-import SSRF** — importing from a remote URL; allowlist and metadata-endpoint exposure.
- **Blob deserialization**, **CSV/formula injection**, **EXIF** handling, and **download
  authorization** (can A fetch B's file?).

## Rules
- Prepare only agreed, **small, inert** test inputs **in memory** — no local fixtures or archive
  artifacts on disk (`docs/write-boundary.md`). For browser-rendering claims use only the benign
  markers agreed for browser testing, in an isolated nonpersistent context.
- Download/serve authorization reuses matched control/test pairs and the A/B accounts from
  `docs/test-accounts.md`; report cross-account file access as a horizontal authz failure.
- Every mutation reversible with a separate read + rollback. No harm to real stored data.

Fold all results and evidence into the single report (`docs/report-standard.md`), written in **English by default** (or the user's chosen language).
