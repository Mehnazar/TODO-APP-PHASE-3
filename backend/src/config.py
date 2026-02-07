"""
Application configuration for Phase III chatbot.

References:
- specs/api/mcp-tools.md
- specs/api/chat-endpoint.md
"""
from dataclasses import dataclass
import os
from pathlib import Path
from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    """Runtime configuration loaded from environment variables."""
    openai_api_key: str
    openai_model: str
    mcp_server_name: str
    mcp_server_version: str


def get_settings(require_openai: bool = True) -> Settings:
    """
    Load configuration from environment variables.

    Raises:
        RuntimeError: If required variables are missing
    """
    env_path = Path(__file__).resolve().parents[1] / ".env"
    load_dotenv(dotenv_path=env_path)

    openai_api_key = os.getenv("OPENAI_API_KEY", "")
    if require_openai and not openai_api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable is required")

    openai_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    mcp_server_name = os.getenv("MCP_SERVER_NAME", "todo-mcp")
    mcp_server_version = os.getenv("MCP_SERVER_VERSION", "0.1.0")

    return Settings(
        openai_api_key=openai_api_key,
        openai_model=openai_model,
        mcp_server_name=mcp_server_name,
        mcp_server_version=mcp_server_version,
    )
