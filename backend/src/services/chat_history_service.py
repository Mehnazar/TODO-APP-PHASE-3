"""
Chat history persistence service.

References: specs/api/chat-endpoint.md
"""
from datetime import datetime, timezone
from typing import Optional, List
import logging

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.models import Conversation, Message


async def get_or_create_conversation(
    user_id: str,
    conversation_id: Optional[int],
    db: AsyncSession,
) -> Conversation:
    """
    Load an existing conversation or create a new one.

    Args:
        user_id: Authenticated user ID
        conversation_id: Existing conversation ID or None
        db: Async database session

    Returns:
        Conversation: The loaded or newly created conversation

    Raises:
        HTTPException: 404 if conversation not found or not owned by user
    """
    logger = logging.getLogger(__name__)
    now = datetime.utcnow()
    if conversation_id is None:
        conversation = Conversation(user_id=user_id, created_at=now, updated_at=now)
        db.add(conversation)
        await db.commit()
        await db.refresh(conversation)
        logger.info("Created new conversation %s for user %s", conversation.id, user_id)
        return conversation

    result = await db.execute(
        select(Conversation)
        .where(Conversation.id == conversation_id)
        .where(Conversation.user_id == user_id)
    )
    conversation = result.scalar_one_or_none()
    if not conversation:
        error_timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": {
                    "code": "CONVERSATION_NOT_FOUND",
                    "message": "Conversation not found",
                    "details": {"conversation_id": conversation_id, "user_id": user_id},
                    "timestamp": error_timestamp,
                }
            },
        )
    logger.info("Loaded conversation %s for user %s", conversation.id, user_id)
    return conversation


async def load_conversation_messages(
    conversation_id: int,
    user_id: str,
    db: AsyncSession,
) -> List[Message]:
    """
    Load message history for a conversation.

    Args:
        conversation_id: Conversation ID
        user_id: Authenticated user ID
        db: Async database session
    """
    logger = logging.getLogger(__name__)
    result = await db.execute(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .where(Message.user_id == user_id)
        .order_by(Message.created_at.asc())
    )
    messages = list(result.scalars().all())
    logger.info("Loaded %s messages for conversation %s", len(messages), conversation_id)
    return messages


async def save_message(
    conversation_id: int,
    user_id: str,
    role: str,
    content: str,
    db: AsyncSession,
) -> Message:
    """
    Persist a single chat message and update conversation timestamp.

    Args:
        conversation_id: Conversation ID
        user_id: Authenticated user ID
        role: Message role ("user" or "assistant")
        content: Message content
        db: Async database session
    """
    logger = logging.getLogger(__name__)
    now = datetime.utcnow()
    message = Message(
        conversation_id=conversation_id,
        user_id=user_id,
        role=role,
        content=content,
        created_at=now,
    )
    db.add(message)

    result = await db.execute(
        select(Conversation)
        .where(Conversation.id == conversation_id)
        .where(Conversation.user_id == user_id)
    )
    conversation = result.scalar_one()
    conversation.updated_at = now

    await db.commit()
    await db.refresh(message)
    logger.info("Saved %s message in conversation %s", role, conversation_id)
    return message
