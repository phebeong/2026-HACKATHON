"""Resource registration aggregator."""

from fema_oversight.resources import provenance


def register_resources(mcp) -> None:
    provenance.register(mcp)
