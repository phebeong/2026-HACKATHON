"""Server configuration loaded from environment variables or a .env file."""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """MCP server settings. Override any field via environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Transport: "stdio" (local) or "streamable-http" (remote/cloud).
    mcp_transport: str = "stdio"
    mcp_host: str = "0.0.0.0"
    mcp_port: int = 8000

    # OpenFEMA requires no API key (public data). The default page size the
    # tools pull before computing review indicators client-side. Keep modest
    # so live demos stay responsive.
    openfema_page_size: int = 1000


settings = Settings()
