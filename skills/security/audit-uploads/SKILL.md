---
name: audit-uploads
description: Audit the upload → storage → processing → serving pipeline of a backend — file-type/path handling, archive extraction (zip-slip), SSRF on URL import, EXIF/CSV-formula injection, and download authorization. Use when the user wants file-upload security review or runs /audit-uploads.
---

# Upload / storage / processing / serving security

Focused skill for the file pipeline. Read first: `references/write-boundary.md`,
`references/test-accounts.md`, `references/report-standard.md`, `references/findings-quality.md` (confidence & export).

## How this skill starts
Follow `references/intake.md`: locate the upload/storage/serving endpoints yourself read-only,
then ask the user — one round of numbered `Q1/Q2…` questions with recommended answers —
only the gaps (authorized test env, upload/download endpoints, accounts A/B, agreed small
inert test inputs, authorized reversible actions). Explain the pipeline tests, then upload
or mutate **only after an explicit "boshla"/"go".** Static review may proceed before that. If the
processing toolchain (e.g. `ogr2ogr`/GDAL, ImageMagick, ffmpeg, libreoffice) is not installed
or the processor is unreachable, mark the dependent processing/serving tests `blocked` — that
is a first-class blocker, not a skip. If there is no env/accounts/human, follow
`references/intake.md` "Static-only engagement".

## Checks
- **Type & name handling** — content-type vs real content, extension/MIME confusion, dangerous
  filenames, path traversal in stored path, overwrite containment.
- **Archive extraction** — zip-slip, nested/symlink entries, path/overwrite containment, and
  expanded-size/ratio/count limits. ZIP creation does **not** prove extraction exists. **Do not
  create or execute decompression bombs.**
- **Post-upload serving** — rendering/serving of internal executable/HTML/SVG files, content
  disposition, and the origin files are served from.
- **SSRF (HTTP and library-level)** — not only an explicit "import from URL" endpoint: a
  processing library can fetch remote resources from inside a file, e.g. GDAL VRT/`/vsicurl`,
  XML external entities (XXE), SVG/`<image href>`, PDF/`ImageMagick` remote refs. Check
  allowlists, disabled-protocol flags, and metadata-endpoint exposure. Use only agreed in-scope targets.
- **Blob deserialization**, **CSV/formula injection**, **EXIF** handling, and **download
  authorization** (can A fetch B's file?).

## Rules
- Prepare only agreed, **small, inert** test inputs **in memory** — no local fixtures or archive
  artifacts on disk (`references/write-boundary.md`). For browser-rendering claims use only the benign
  markers agreed for browser testing, in an isolated nonpersistent context.
- Download/serve authorization reuses matched control/test pairs and the A/B accounts from
  `references/test-accounts.md`; report cross-account file access as a horizontal authz failure.
- Every mutation reversible with a separate read + rollback. No harm to real stored data.

Fold all results and evidence into the single report (`references/report-standard.md`), written in **English by default** (or the user's chosen language).
