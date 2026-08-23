from typing import Any

from src.core.outbox.models import OutboxEvent


def build_outbox_event(
	aggregatetype: str,
	aggregateid: str,
	event_type: str,
	payload: dict[str, Any] | None,
) -> OutboxEvent:
	return OutboxEvent(
		aggregatetype=aggregatetype,
		aggregateid=aggregateid,
		type=event_type,
		payload=payload,
	)
