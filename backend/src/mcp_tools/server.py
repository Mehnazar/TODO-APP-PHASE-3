"""
MCP server setup for Phase III tools.

References: specs/api/mcp-tools.md
"""
from typing import Any, Dict, Optional

from mcp.server.fastmcp import FastMCP

from src.config import get_settings
from src.db import async_session
from src.mcp_tools import tools as mcp_tools


settings = get_settings(require_openai=False)
mcp_server = FastMCP(settings.mcp_server_name)


@mcp_server.tool()
async def add_task(user_id: str, title: str, description: Optional[str] = None) -> Dict[str, Any]:
    """Create a new task."""
    async with async_session() as session:
        return await mcp_tools.add_task(user_id=user_id, title=title, description=description, db=session)


@mcp_server.tool()
async def list_tasks(user_id: str, status: Optional[str] = None) -> Dict[str, Any]:
    """List tasks for a user."""
    async with async_session() as session:
        return await mcp_tools.list_tasks(user_id=user_id, status=status, db=session)


@mcp_server.tool()
async def update_task(
    user_id: str,
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
) -> Dict[str, Any]:
    """Update a task."""
    async with async_session() as session:
        return await mcp_tools.update_task(
            user_id=user_id,
            task_id=task_id,
            title=title,
            description=description,
            db=session,
        )


@mcp_server.tool()
async def complete_task(user_id: str, task_id: int) -> Dict[str, Any]:
    """Mark a task as completed."""
    async with async_session() as session:
        return await mcp_tools.complete_task(user_id=user_id, task_id=task_id, db=session)


@mcp_server.tool()
async def delete_task(user_id: str, task_id: int) -> Dict[str, Any]:
    """Delete a task."""
    async with async_session() as session:
        return await mcp_tools.delete_task(user_id=user_id, task_id=task_id, db=session)


def get_mcp_server() -> FastMCP:
    """Return the configured MCP server instance."""
    return mcp_server
