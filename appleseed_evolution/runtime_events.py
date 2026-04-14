from __future__ import annotations

from typing import Any

from appleseed_evolution.openclaw_contract import (
    ALLOWED_OPENCLAW_APPLESEED_EVENT_KINDS,
    ALLOWED_OPENCLAW_APPLESEED_FEEDBACK_STATUSES,
    OPENCLAW_APPLESEED_EVENT_SCHEMA_VERSION,
    OpenClawAppleseedEventEnvelope,
    parse_openclaw_appleseed_event_envelopes,
)

RUNTIME_EVENT_SCHEMA_VERSION = OPENCLAW_APPLESEED_EVENT_SCHEMA_VERSION
ALLOWED_RUNTIME_EVENT_KINDS = ALLOWED_OPENCLAW_APPLESEED_EVENT_KINDS
ALLOWED_RUNTIME_FEEDBACK_STATUSES = ALLOWED_OPENCLAW_APPLESEED_FEEDBACK_STATUSES
RuntimeSessionEvent = OpenClawAppleseedEventEnvelope


def parse_runtime_session_events(payload: Any) -> list[RuntimeSessionEvent]:
    return parse_openclaw_appleseed_event_envelopes(payload)
