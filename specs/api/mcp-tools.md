# MCP Tools Specification: Phase III Chatbot

**Feature Branch**: `001-phase3-chatbot`  
**Created**: 2026-02-07  
**Status**: Draft  
**Input**: User description: "Create specs/api/mcp-tools.md for Phase III. Define MCP tools: add_task, list_tasks, update_task, complete_task, delete_task. Include purpose, parameters, return values, and example input/output. Tools must be stateless and persist data using the database."

## Purpose & Scope *(mandatory)*

Define the MCP tools exposed by the Phase III chatbot server to support task CRUD via natural language. Tools are stateless and persist all data in the database.

## Tool Standards *(mandatory)*

- Tools MUST be stateless; no in-memory state is retained between calls.
- Tools MUST persist task data to the database.
- Tools MUST accept `user_id` as the first parameter.
- Tools MUST return structured JSON responses.

## Tool Definitions *(mandatory)*

### 1) add_task

**Purpose**: Create a new task for the specified user.

**Parameters**:

- `user_id` (string, required): ID of the authenticated user
- `title` (string, required): Task title (1–200 characters)
- `description` (string, optional): Task description (max 1000 characters)

**Return Values**:

- `task_id` (integer): ID of the created task
- `status` (string): "created"
- `title` (string): Task title

**Example Input**:

```json
{
  "user_id": "user_123",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

**Example Output**:

```json
{
  "task_id": 1,
  "status": "created",
  "title": "Buy groceries"
}
```

---

### 2) list_tasks

**Purpose**: Retrieve tasks for the specified user, optionally filtered by status.

**Parameters**:

- `user_id` (string, required): ID of the authenticated user
- `status` (string, optional): "all" | "pending" | "completed"

**Return Values**:

- Array of task items with:
  - `id` (integer)
  - `title` (string)
  - `completed` (boolean)

**Example Input**:

```json
{
  "user_id": "user_123",
  "status": "completed"
}
```

**Example Output**:

```json
[
  { "id": 2, "title": "Call mom", "completed": true },
  { "id": 5, "title": "Finish report", "completed": true }
]
```

---

### 3) update_task

**Purpose**: Update the title and/or description of an existing task.

**Parameters**:

- `user_id` (string, required): ID of the authenticated user
- `task_id` (integer, required): ID of the task to update
- `title` (string, optional): New title (1–200 characters)
- `description` (string, optional): New description (max 1000 characters)

**Return Values**:

- `task_id` (integer)
- `status` (string): "updated"
- `title` (string)

**Example Input**:

```json
{
  "user_id": "user_123",
  "task_id": 3,
  "title": "Buy groceries and fruits"
}
```

**Example Output**:

```json
{
  "task_id": 3,
  "status": "updated",
  "title": "Buy groceries and fruits"
}
```

---

### 4) complete_task

**Purpose**: Mark a task as completed for the specified user.

**Parameters**:

- `user_id` (string, required): ID of the authenticated user
- `task_id` (integer, required): ID of the task to complete

**Return Values**:

- `task_id` (integer)
- `status` (string): "completed"
- `title` (string)

**Example Input**:

```json
{
  "user_id": "user_123",
  "task_id": 1
}
```

**Example Output**:

```json
{
  "task_id": 1,
  "status": "completed",
  "title": "Buy groceries"
}
```

---

### 5) delete_task

**Purpose**: Remove a task for the specified user.

**Parameters**:

- `user_id` (string, required): ID of the authenticated user
- `task_id` (integer, required): ID of the task to delete

**Return Values**:

- `task_id` (integer)
- `status` (string): "deleted"
- `title` (string)

**Example Input**:

```json
{
  "user_id": "user_123",
  "task_id": 2
}
```

**Example Output**:

```json
{
  "task_id": 2,
  "status": "deleted",
  "title": "Call mom"
}
```
