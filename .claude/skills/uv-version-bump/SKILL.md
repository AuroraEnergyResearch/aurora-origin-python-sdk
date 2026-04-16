---
name: uv-version-bump
description: Handle Python project version bumping with uv in repositories that use pyproject.toml and uv.lock. Use when asked to bump versions, cut patch/minor/major releases, or sync lockfiles after version changes.
---

# UV Version Bump

Use this workflow for projects managed by `uv`.

## Bump workflow

1. Confirm project root contains `pyproject.toml`.
2. Read current project version:
   - `uv version`
   - optional: `uv version --short`
3. Preview intended bump before applying:
   - `uv version --bump patch --dry-run`
4. Apply bump:
   - Semver bump: `uv version --bump patch|minor|major`
   - Exact version: `uv version <x.y.z>`
5. Regenerate lock metadata:
   - `uv lock`
6. Verify lock consistency:
   - `uv lock --check`
7. Confirm changed files include both:
   - `pyproject.toml`
   - `uv.lock`

## Supported bump components

Use `--bump` with:
- `major`, `minor`, `patch`
- `stable`, `alpha`, `beta`, `rc`, `post`, `dev`

You can pass more than one bump component; uv applies them from largest to smallest.

## Rules

- Do not edit `uv.lock` manually.
- Prefer `uv version --bump ...` over hand-editing version fields.
- When repository policy requires, run the project’s focused tests after bumping.
