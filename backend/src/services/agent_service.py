"""
OpenAI Agents SDK orchestration for chat requests.

References:
- specs/features/chatbot.md
- specs/api/mcp-tools.md
"""
from dataclasses import dataclass
from typing import List, Optional
import logging
import asyncio
import os

from src.config import get_settings
from src.db import async_session
from src.mcp_tools import tools as mcp_tools
from src.models import Message


@dataclass(frozen=True)
class AgentResult:
    """Result of an agent run."""
    response: str
    tool_calls: List[str]


def _format_history(messages: List[Message]) -> str:
    """Flatten message history into a plain-text context block."""
    lines: List[str] = []
    for message in messages:
        lines.append(f"{message.role}: {message.content}")
    return "\n".join(lines)


async def run_agent(
    user_id: str,
    message: str,
    history: List[Message],
) -> AgentResult:
    """
    Run the OpenAI Agent with MCP tools and return a response.

    Args:
        user_id: Authenticated user ID
        message: Current user message
        history: Prior conversation messages
    """
    logger = logging.getLogger(__name__)
    try:
        settings = get_settings()
        if settings.openai_api_key:
            os.environ["OPENAI_API_KEY"] = settings.openai_api_key
        from agents import Agent, Runner
        from agents.tool import function_tool
    except Exception as exc:
        logger.exception("Agent initialization failed")
        return AgentResult(
            response="Sorry, the AI service is temporarily unavailable. Please try again.",
            tool_calls=[],
        )

    @function_tool
    async def add_task(title: str, description: Optional[str] = None):
        async with async_session() as session:
            return await mcp_tools.add_task(user_id=user_id, title=title, description=description, db=session)

    @function_tool
    async def list_tasks(status: Optional[str] = None):
        async with async_session() as session:
            return await mcp_tools.list_tasks(user_id=user_id, status=status, db=session)

    @function_tool
    async def update_task(task_id: int, title: Optional[str] = None, description: Optional[str] = None):
        async with async_session() as session:
            return await mcp_tools.update_task(
                user_id=user_id,
                task_id=task_id,
                title=title,
                description=description,
                db=session,
            )

    @function_tool
    async def complete_task(task_id: int):
        async with async_session() as session:
            return await mcp_tools.complete_task(user_id=user_id, task_id=task_id, db=session)

    @function_tool
    async def delete_task(task_id: int):
        async with async_session() as session:
            return await mcp_tools.delete_task(user_id=user_id, task_id=task_id, db=session)

    instructions = (
        "You are a friendly task assistant. Interpret user intent, "
        "call the correct tool(s), and confirm actions concisely. "
        "If intent is ambiguous, ask a clarification question. "
        "Use the provided tools for task operations."
    )
    history_block = _format_history(history)
    prompt = f"Conversation so far:\n{history_block}\n\nUser: {message}"

    agent = Agent(
        name="TodoChatAgent",
        instructions=instructions,
        model=settings.openai_model,
        tools=[add_task, list_tasks, update_task, complete_task, delete_task],
    )

    logger.info("Running agent for user %s", user_id)
    try:
        result = await asyncio.wait_for(Runner.run(agent, input=prompt), timeout=10)
        response_text = getattr(result, "output_text", None) or getattr(result, "output", None) or str(result)
        tool_calls = []
        if hasattr(result, "tool_calls"):
            tool_calls = [call.name for call in result.tool_calls]
        logger.info("Agent completed for user %s with tools %s", user_id, tool_calls)
        return AgentResult(response=response_text, tool_calls=tool_calls)
    except Exception as exc:
        logger.exception("Agent failed for user %s", user_id)
        return AgentResult(
            response="Sorry, the AI service is temporarily unavailable. Please try again.",
            tool_calls=[],
        )
