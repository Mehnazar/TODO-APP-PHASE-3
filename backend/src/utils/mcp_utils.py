"""
Helpers for standardized MCP tool responses.

References: specs/api/mcp-tools.md
"""
from datetime import datetime, timezone
from typing import Any, Dict


def _timestamp() -> str:
    """Return current UTC timestamp in ISO 8601 with Z suffix."""
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def success_response(tool: str, user_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Build standardized success response for MCP tools.

    Args:
        tool: Tool name
        user_id: Authenticated user ID
        data: Payload data to return
    """
    return {
        "success": True,
        "data": data,
        "metadata": {
            "timestamp": _timestamp(),
            "tool": tool,
            "user_id": user_id,
        },
    }


def error_response(
    tool: str,
    code: str,
    message: str,
    details: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Build standardized error response for MCP tools.

    Args:
        tool: Tool name
        code: Error code string
        message: User-friendly error message
        details: Error detail payload
    """
    return {
        "success": False,
        "error": {
            "code": code,
            "message": message,
            "details": details,
        },
        "metadata": {
            "timestamp": _timestamp(),
            "tool": tool,
        },
    }
