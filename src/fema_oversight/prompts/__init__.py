"""Prompt registration aggregator."""

from fema_oversight.prompts import oversight_review


def register_prompts(mcp) -> None:
    oversight_review.register(mcp)
