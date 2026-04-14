# Appleseed Evolution

[🇨🇳 中文文档](README_zh.md)

**Appleseed Evolution is a governed evolution layer for OpenClaw, Appleseed Memory, and similar agent runtimes.**

It helps operators ingest runtime evidence, audit what happened, generate conservative evolution proposals, review promotion risk, and resume work safely after interruption or restart.

In plain English:
- **What it is:** a local operator control plane for agent evolution
- **What it is not:** an "autonomous self-improving AGI" claim
- **Who it is for:** people building serious agent systems who care about auditability, rollback, recovery, and human control

## Why this repo exists

Most "agent evolution" demos stop at:
- proxying model calls
- injecting skills
- telling a story about automatic improvement

Appleseed Evolution goes after the harder operator problems:
- **runtime feedback ingestion**
- **raw vs projected evidence separation**
- **reviewable proposal generation**
- **explicit governance and rollback context**
- **restart-safe workflow state**
- **handoff bundles that can be replayed later**

That makes this repo much more useful for real operations around **OpenClaw**, **Appleseed**, and other long-running agent systems.

## What Appleseed Evolution does

Appleseed Evolution sits **beside** your runtime instead of replacing it.

1. A task or runtime artifact comes in through the CLI, local proxy, or `openclaw-import` path.
2. The system stores raw evidence in append-only ledgers.
3. Supported signals are projected into a separate evolution-feedback ledger.
4. The operator can inspect the raw → projected audit path.
5. Appleseed Evolution generates conservative proposals and gates them.
6. The operator reviews readiness, risk, and rollback context before promotion.
7. Workflow state and handoff bundles are persisted so work can continue after restart or ownership handoff.

So the right mental model is:

> **Appleseed Evolution = governed local evolution pipeline for agent systems**

Not:
- end-to-end autonomous learning
- online RL platform
- self-modifying production autopilot

## Who should use this

Use Appleseed Evolution if you want:
- a local **agent evolution framework**
- a safer **OpenClaw skill / prompt evolution** workflow
- an **Appleseed Memory**-friendly evidence and audit layer
- better **operator workflow** around review, promotion, rollback, and restart recovery

Do **not** pick this expecting:
- cloud training
- OPD / RL loops
- magical autonomous improvement with no operator review

## Key features in v1.1

### Runtime ingest and audit
- typed runtime event schema
- CLI ingest from file or stdin
- local HTTP ingest endpoint
- raw inbound envelope ledger
- projected feedback ledger
- inspect command for raw → projected audit

### OpenClaw / Appleseed integration surface
- formal OpenClaw/Appleseed contract
- `openclaw-import` for realistic OpenClaw operator session artifacts
- report output that surfaces OpenClaw handoff context
- replayable operator handoff bundles
- official in-repo OpenClaw plugin package for export / spool / transport

### Governance and operator control
- proposal generation with conservative gate logic
- governance metadata for readiness / risk / rollback
- review queue with ready / risky / rollback-sensitive / blocked buckets
- reviewable promotion artifacts
- dry-run promotion support
- restart-safe workflow state
- `resume` command for restart recovery

## Quick start

Requires **Python 3.11+**.

You can run this repo directly without a package install.

### 1. List demo skills

```bash
python3 -m appleseed_evolution.cli skills --config demo/appleseed.toml list
```

### 2. Route a task

```bash
python3 -m appleseed_evolution.cli route \
  --config demo/appleseed.toml \
  --task "review this patch for regressions"
```

### 3. Import a realistic OpenClaw operator session

```bash
python3 -m appleseed_evolution.cli openclaw-import \
  --config demo/appleseed.toml \
  --file demo/openclaw_sessions/sample_operator_session.json
```

### 4. Inspect, review, and resume

```bash
python3 -m appleseed_evolution.cli inspect --config demo/appleseed.toml --write-report
python3 -m appleseed_evolution.cli review --config demo/appleseed.toml --format markdown --write-report
python3 -m appleseed_evolution.cli resume --config demo/appleseed.toml
```

### 5. Generate and promote conservative proposals

```bash
python3 -m appleseed_evolution.cli evolve --config demo/appleseed.toml
python3 -m appleseed_evolution.cli governance --config demo/appleseed.toml --format markdown --write-report
python3 -m appleseed_evolution.cli promote --config demo/appleseed.toml --proposal-id prompt-code_review --dry-run --write-report
```

## Most important commands

### Runtime evidence
```bash
python3 -m appleseed_evolution.cli ingest --config demo/appleseed.toml --file demo/runtime_events/sample_batch.json
python3 -m appleseed_evolution.cli openclaw-import --config demo/appleseed.toml --file demo/openclaw_sessions/sample_operator_session.json
python3 -m appleseed_evolution.cli report --config demo/appleseed.toml --file demo/runtime_events/sample_batch.json --format markdown --write-report
python3 -m appleseed_evolution.cli inspect --config demo/appleseed.toml --write-report
```

### Governance and promotion
```bash
python3 -m appleseed_evolution.cli evolve --config demo/appleseed.toml
python3 -m appleseed_evolution.cli governance --config demo/appleseed.toml --format markdown --write-report
python3 -m appleseed_evolution.cli review --config demo/appleseed.toml --format markdown --write-report
python3 -m appleseed_evolution.cli promote --config demo/appleseed.toml --proposal-id prompt-code_review --dry-run --write-report
python3 -m appleseed_evolution.cli resume --config demo/appleseed.toml
```

### Local HTTP surface
```bash
python3 -m appleseed_evolution.cli serve --config demo/appleseed.toml
curl http://127.0.0.1:8765/health
```

## Architecture

```text
appleseed_evolution/
  cli.py                 # Local CLI entrypoint
  config.py              # TOML config loader
  models.py              # Shared dataclasses
  openclaw_contract.py   # Formal OpenClaw/Appleseed contract + typed models
  runtime_events.py      # Runtime-event parsing compatibility layer
  skill_bank.py          # Skill loading + deterministic retrieval
  feedback_store.py      # Append-only ledgers + audit helpers
  workflow_state.py      # Restart-safe workflow checkpoint helpers
  evolution/
    prompt_evolver.py    # Heuristic prompt/skill metadata proposals
    workflow_discoverer.py
    capability_assessor.py
    evaluator.py         # Offline evaluation gate
    governance.py        # Readiness / risk / rollback metadata
    pipeline.py          # Proposal generation + promotion logic
  runtime/
    openclaw_adapter.py  # OpenClaw operator-session adapter + handoff builder
    orchestrator.py      # Runtime/evolution glue
    proxy.py             # Minimal local HTTP server
    report_adapter.py    # Operator evidence bundle adapter
integrations/
  openclaw-plugin/       # Official OpenClaw plugin package for Appleseed export/spool/transport

## Official OpenClaw plugin v0.1

Appleseed Evolution now includes its first official OpenClaw integration package at `integrations/openclaw-plugin`.

The boundary is deliberate:
- **Appleseed Evolution remains the control plane**
- the OpenClaw plugin stays thin and only handles export, spool, and transport
- no LLM calls, cloud loops, or self-modifying behavior live inside the plugin

The plugin exposes:
- `openclaw appleseed-export ...` CLI commands
- `appleseedEvolution.export` and `appleseedEvolution.status` Gateway RPC methods
- `/appleseed-evolution/export` and `/appleseed-evolution/status` plugin HTTP routes
- append-only JSONL spool files for runtime events, operator-session artifacts, support capture, and delivery attempts

Runtime-event payloads can POST directly into Appleseed Evolution's local `/v1/ingest`.
`openclaw_operator_session` artifacts stay spooled in v0.1 and are replayed through `python3 -m appleseed_evolution.cli openclaw-import`, because Appleseed' local HTTP surface does not expose that richer import path yet.

Local plugin verification is dependency-light:

```bash
cd integrations/openclaw-plugin
npm test
npm run verify:fixtures
npm run pack:dry-run
```

## Honest scope

### Implemented in v1.1
- local TOML config loading
- skill manifests from JSON
- deterministic local retrieval
- append-only event and feedback storage
- formal OpenClaw/Appleseed contract
- local CLI and HTTP ingest
- explicit `openclaw-import` command
- JSON / markdown operator evidence reports
- operator-visible inspect command
- offline evaluation gate
- governance metadata and review queue
- promotion artifacts and dry-run support
- restart-safe workflow state with resume commands
- replayable operator handoff bundles

### Deliberately not shipped in v1.1
- no online RL
- no OPD
- no cloud training
- no blind self-modification
- no benchmark-backed evaluator yet
- no automatic deployment into production runtimes yet

## Key docs
- [`docs/v1_1_milestone.md`](docs/v1_1_milestone.md) — what v1.1 ships and why it matters
- [`docs/v1_2_productization_roadmap.md`](docs/v1_2_productization_roadmap.md) — next productization slice
- [`docs/openclaw_appleseed_contract.md`](docs/openclaw_appleseed_contract.md) — formal OpenClaw/Appleseed contract
- [`docs/openclaw_plugin_integration.md`](docs/openclaw_plugin_integration.md) — official OpenClaw plugin transport/export workflow
- [`docs/operator_review_workflow.md`](docs/operator_review_workflow.md) — review / promotion workflow
- [`CHANGELOG.md`](CHANGELOG.md) — versioned project history

## Testing

```bash
python3 -m unittest discover -s tests -v
```

Current coverage focuses on:
- config path resolution
- skill retrieval relevance
- runtime ingest behavior
- raw → projected audit inspection
- governance / review / promotion behavior
- restart recovery and handoff replay
- OpenClaw operator session import

## Project status

Appleseed Evolution v1.1 is now a **runnable local operator-grade evolution system** for Appleseed/OpenClaw-style runtimes.

It is already useful for:
- governed local demos
- runtime evidence capture
- operator review workflows
- promotion with rollback context
- restart-safe continuation and handoff

It is **not yet** the final production product. The next step is productization: tighter operator cockpit, stronger handoff packaging, and harder promotion gates.
