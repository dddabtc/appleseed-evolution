# Operator Review and Promote Workflow

Atlas Evolution keeps proposal review and promotion local, deterministic, and operator-visible.

## Command Chain

Generate or refresh the latest evolution report:

```bash
python3 -m atlas_evolution.cli evolve --config demo/atlas.toml
```

Inspect the compact governance summary:

```bash
python3 -m atlas_evolution.cli governance \
  --config demo/atlas.toml \
  --format markdown \
  --write-report
```

Build the operator review queue with change previews:

```bash
python3 -m atlas_evolution.cli review \
  --config demo/atlas.toml \
  --format markdown \
  --write-report
```

Dry-run a targeted promotion artifact:

```bash
python3 -m atlas_evolution.cli promote \
  --config demo/atlas.toml \
  --proposal-id prompt-code_review \
  --dry-run \
  --write-report
```

Apply the reviewed proposal:

```bash
python3 -m atlas_evolution.cli promote \
  --config demo/atlas.toml \
  --proposal-id prompt-code_review \
  --write-report
```

## Review Buckets

- `ready`: approved proposals that have a local automatic promotion path.
- `risky`: approved proposals whose gate result is still `medium` or `high` risk.
- `rollback_sensitive`: proposals with an explicit local rollback target and revert steps.
- `operator_review_required`: scaffolded proposals that stay manual-review only.
- `blocked`: proposals that failed the gate and should not be promoted.

## Promotion Artifact Contents

`promote` now emits a deterministic artifact that records:

- the source evolution report
- whether the run was a dry run
- which proposal IDs were requested
- which proposals were selected vs skipped
- the diff preview and operation summary for each selected prompt update
- rollback steps for each selected proposal
- the files actually changed during a non-dry-run promotion

This keeps the promotion surface reviewable even when no files are changed.
