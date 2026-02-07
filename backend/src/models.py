"""
SQLModel database models.

References: specs/database/schema.md
"""
from sqlmodel import Field, SQLModel
from datetime import datetime
from typing import Optional


class User(SQLModel, table=True):
    """
    User model for authentication.

    Managed by Better Auth in Phase II.
    All timestamps stored in UTC as timezone-naive datetimes.
    """
    __tablename__ = "users"

    id: str = Field(primary_key=True)  # Better Auth format: usr_xxxxx
    email: str = Field(unique=True, index=True)
    name: Optional[str] = None
    password_hash: str = Field()  # Bcrypt hashed password
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Task(SQLModel, table=True):
    """
    Task model for todo items.

    All timestamps stored in UTC as timezone-naive datetimes (per CONSTITUTION.md timezone handling).
    """
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=200)
    description: str = Field(default="", max_length=1000)
    completed: bool = Field(default=False, index=True)
    priority: str = Field(default="medium", max_length=20)  # low, medium, high
    category: Optional[str] = Field(default=None, max_length=50)
    due_date: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Conversation(SQLModel, table=True):
    """
    Conversation model for chat sessions.

    Conversation state is reconstructed from database rows per request.
    """
    __tablename__ = "conversations"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, index=True)


class Message(SQLModel, table=True):
    """
    Message model for chat conversation history.

    Stores user and assistant messages linked to a conversation.
    """
    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversations.id", index=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    role: str = Field(max_length=20)
    content: str = Field()
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
