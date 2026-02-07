"""
MCP tool implementations for task operations.

References: specs/api/mcp-tools.md
"""
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.models import Task
from src.utils.mcp_utils import success_response, error_response


async def add_task(
    user_id: str,
    title: str,
    description: Optional[str],
    db: AsyncSession,
) -> Dict[str, Any]:
    """Create a new task for the user."""
    if not title or len(title) > 200:
        return error_response(
            tool="add_task",
            code="VALIDATION_ERROR",
            message="Title must be between 1 and 200 characters.",
            details={"title": title, "user_id": user_id},
        )
    if description is not None and len(description) > 1000:
        return error_response(
            tool="add_task",
            code="VALIDATION_ERROR",
            message="Description must be 1000 characters or less.",
            details={"user_id": user_id},
        )

    now = datetime.now(timezone.utc)
    task = Task(
        user_id=user_id,
        title=title,
        description=description or "",
        completed=False,
        created_at=now,
        updated_at=now,
    )
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return success_response(
        tool="add_task",
        user_id=user_id,
        data={"task_id": task.id, "status": "created", "title": task.title},
    )


async def list_tasks(
    user_id: str,
    status: Optional[str],
    db: AsyncSession,
) -> Dict[str, Any]:
    """List tasks for the user with optional status filter."""
    status_filter = (status or "all").lower()
    query = select(Task).where(Task.user_id == user_id)
    if status_filter == "pending":
        query = query.where(Task.completed == False)  # noqa: E712
    elif status_filter == "completed":
        query = query.where(Task.completed == True)  # noqa: E712
    elif status_filter != "all":
        return error_response(
            tool="list_tasks",
            code="VALIDATION_ERROR",
            message="Status must be one of: all, pending, completed.",
            details={"status": status, "user_id": user_id},
        )

    result = await db.execute(query.order_by(Task.created_at.asc()))
    tasks = result.scalars().all()
    data: List[Dict[str, Any]] = [
        {"id": task.id, "title": task.title, "completed": task.completed}
        for task in tasks
    ]
    return success_response(
        tool="list_tasks",
        user_id=user_id,
        data={"tasks": data, "status": status_filter},
    )


async def update_task(
    user_id: str,
    task_id: int,
    title: Optional[str],
    description: Optional[str],
    db: AsyncSession,
) -> Dict[str, Any]:
    """Update a task's title and/or description."""
    if title is not None and (len(title) == 0 or len(title) > 200):
        return error_response(
            tool="update_task",
            code="VALIDATION_ERROR",
            message="Title must be between 1 and 200 characters.",
            details={"task_id": task_id, "user_id": user_id},
        )
    if description is not None and len(description) > 1000:
        return error_response(
            tool="update_task",
            code="VALIDATION_ERROR",
            message="Description must be 1000 characters or less.",
            details={"task_id": task_id, "user_id": user_id},
        )

    result = await db.execute(
        select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
    )
    task = result.scalar_one_or_none()
    if not task:
        return error_response(
            tool="update_task",
            code="TASK_NOT_FOUND",
            message="Task not found.",
            details={"task_id": task_id, "user_id": user_id},
        )

    if title is not None:
        task.title = title
    if description is not None:
        task.description = description
    task.updated_at = datetime.now(timezone.utc)

    await db.commit()
    await db.refresh(task)
    return success_response(
        tool="update_task",
        user_id=user_id,
        data={"task_id": task.id, "status": "updated", "title": task.title},
    )


async def complete_task(
    user_id: str,
    task_id: int,
    db: AsyncSession,
) -> Dict[str, Any]:
    """Mark a task as completed."""
    result = await db.execute(
        select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
    )
    task = result.scalar_one_or_none()
    if not task:
        return error_response(
            tool="complete_task",
            code="TASK_NOT_FOUND",
            message="Task not found.",
            details={"task_id": task_id, "user_id": user_id},
        )

    task.completed = True
    task.updated_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(task)
    return success_response(
        tool="complete_task",
        user_id=user_id,
        data={"task_id": task.id, "status": "completed", "title": task.title},
    )


async def delete_task(
    user_id: str,
    task_id: int,
    db: AsyncSession,
) -> Dict[str, Any]:
    """Delete a task for the user."""
    result = await db.execute(
        select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
    )
    task = result.scalar_one_or_none()
    if not task:
        return error_response(
            tool="delete_task",
            code="TASK_NOT_FOUND",
            message="Task not found.",
            details={"task_id": task_id, "user_id": user_id},
        )

    title = task.title
    await db.delete(task)
    await db.commit()
    return success_response(
        tool="delete_task",
        user_id=user_id,
        data={"task_id": task_id, "status": "deleted", "title": title},
    )
