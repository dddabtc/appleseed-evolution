# OpenClaw Plugin Integration

Appleseed Evolution now ships its first official OpenClaw integration package in-repo at:

`integrations/openclaw-plugin`

This is a thin export/spool/transport bridge, not a second control plane.

## Design boundary

Appleseed Evolution stays responsible for:

- raw runtime evidence ledgers
- projection into evolution feedback
- operator review and promotion workflow
- `openclaw-import` adaptation and replay logic

The OpenClaw plugin only handles:

- building Appleseed-compatible export payloads
- append-only local JSONL spooling
- optional POST of runtime-event payloads to Appleseed Evolution's local `/v1/ingest`
- lightweight support capture from documented plugin hooks

The package is intentionally dependency-free at runtime and can be verified from its own directory with:

```bash
cd integrations/openclaw-plugin
npm test
npm run verify:fixtures
npm run pack:dry-run
```

## Why the plugin is explicit instead of magical

The OpenClaw references used for this v0.1 clearly support:

- plugin config via `openclaw.plugin.json`
- plugin HTTP routes
- plugin Gateway RPC methods
- plugin CLI commands
- auto-reply commands
- message / compaction / tool-result hooks

They do **not** document a complete stable lifecycle that already gives Appleseed Evolution all of:

- the operator's true task string
- terminal session outcome
- numeric feedback score
- handoff semantics suitable for `openclaw-import`

So the plugin does not fake those fields by scraping partial runtime state.

Instead, Appleseed-compatible payloads are exported through explicit surfaces:

- `openclaw appleseed-export ...`
- `appleseedEvolution.export`
- `POST /appleseed-evolution/export`

Support telemetry from hooks is still captured locally in `support-capture.jsonl` for audit context.

## Transport matrix

`session_started` / `session_feedback` runtime events:

- spool file: `runtime-events.jsonl`
- optional POST target: `http://127.0.0.1:8765/v1/ingest`
- Appleseed receiver: `python3 -m appleseed_evolution.cli serve --config ...`

`openclaw_operator_session` artifacts:

- spool file: `operator-sessions.jsonl`
- no POST target in v0.1
- Appleseed receiver: `python3 -m appleseed_evolution.cli openclaw-import --file ...` with one artifact object at a time, not the whole JSONL spool file

Delivery attempts are logged in:

- `delivery-attempts.jsonl`

Support hook capture is logged in:

- `support-capture.jsonl`

## OpenClaw load example

```json5
{
  plugins: {
    load: {
      paths: [
        "/home/ubuntu/repos/appleseed-evolution/integrations/openclaw-plugin"
      ]
    },
    entries: {
      "appleseed-evolution": {
        enabled: true,
        config: {
          enabled: true,
          baseUrl: "http://127.0.0.1:8765",
          spoolDir: ".openclaw/appleseed-evolution-spool",
          retry: {
            maxAttempts: 3,
            backoffMs: 250,
            maxBackoffMs: 2000
          },
          includeTranscript: false,
          includeToolCalls: "summary"
        }
      }
    }
  }
}
```

## Appleseed operator workflow

1. Run the Appleseed local HTTP surface if you want direct runtime-event delivery:

```bash
python3 -m appleseed_evolution.cli serve --config demo/appleseed.toml
```

2. Export or spool from OpenClaw:

```bash
openclaw appleseed-export feedback \
  --session-id demo-session-001 \
  --task "review postgres migration rollback safety" \
  --status failure \
  --score 0.2
```

3. For richer operator-session artifacts, import the exported JSON with:

```bash
python3 -m appleseed_evolution.cli openclaw-import \
  --config demo/appleseed.toml \
  --file /path/to/operator-session.json
```

4. Continue the normal Appleseed review chain:

```bash
python3 -m appleseed_evolution.cli inspect --config demo/appleseed.toml --write-report
python3 -m appleseed_evolution.cli review --config demo/appleseed.toml --format markdown --write-report
python3 -m appleseed_evolution.cli promote --config demo/appleseed.toml --proposal-id prompt-code_review --dry-run --write-report
```

## Verification

Fixture and schema verification:

```bash
cd integrations/openclaw-plugin
npm test
npm run verify:fixtures
npm run pack:dry-run
```

Repo-root verification:

```bash
python3 integrations/openclaw-plugin/scripts/verify_payloads.py
python3 -m unittest tests.test_openclaw_plugin_integration -v
```
