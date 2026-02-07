"""
Chat endpoint for Phase III AI chatbot.

References: specs/api/chat-endpoint.md
"""
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone

from src.db import get_session
from src.middleware.auth import get_current_user
from src.services.chat_history_service import (
    get_or_create_conversation,
    load_conversation_messages,
    save_message,
)
from src.services.agent_service import run_agent


router = APIRouter(prefix="/api/v1", tags=["chat"])


class ChatRequest(BaseModel):
    """Request body for chat endpoint."""
    conversation_id: Optional[int] = None
    message: str = Field(min_length=1, max_length=2000)


class ChatResponse(BaseModel):
    """Response body for chat endpoint."""
    conversation_id: int
    response: str
    tool_calls: List[str]


@router.post("/{user_id}/chat", response_model=ChatResponse)
async def chat(
    user_id: str,
    request: ChatRequest,
    current_user: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
) -> ChatResponse:
    """
    Handle a chat message by running the AI agent and persisting history.
    """
    if user_id != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "error": {
                    "code": "FORBIDDEN",
                    "message": "You can only access your own chat history",
                    "details": {"user_id": user_id},
                    "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                }
            },
        )

    conversation = await get_or_create_conversation(
        user_id=user_id,
        conversation_id=request.conversation_id,
        db=db,
    )
    history = await load_conversation_messages(conversation.id, user_id, db)

    await save_message(
        conversation_id=conversation.id,
        user_id=user_id,
        role="user",
        content=request.message,
        db=db,
    )

    agent_result = await run_agent(user_id=user_id, message=request.message, history=history)

    await save_message(
        conversation_id=conversation.id,
        user_id=user_id,
        role="assistant",
        content=agent_result.response,
        db=db,
    )

    return ChatResponse(
        conversation_id=conversation.id,
        response=agent_result.response,
        tool_calls=agent_result.tool_calls,
    )
