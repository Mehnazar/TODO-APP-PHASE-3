# API Specification: Chat Endpoint (Phase III)

**Feature Branch**: `001-phase3-chatbot`  
**Created**: 2026-02-07  
**Status**: Draft  
**Input**: User description: "Create specs/api/chat-endpoint.md. Specify the POST /api/{user_id}/chat endpoint including request schema, response schema, conversation handling, stateless lifecycle, and JWT authentication via Better Auth."

## Purpose & Scope *(mandatory)*

Define the POST chat endpoint that powers the Phase III AI chatbot, including request/response schemas, conversation handling, and stateless lifecycle requirements aligned with Phase II authentication.

## Endpoint Definition *(mandatory)*

**Method**: POST  
**Path**: `/api/{user_id}/chat`

## Authentication Requirements *(mandatory)*

- JWT authentication via Better Auth is required.
- Clients must send `Authorization: Bearer <token>` header.
- The `user_id` in the path MUST match the user identity from the JWT.
- Unauthorized or mismatched requests MUST be rejected.

## Request Schema *(mandatory)*

```json
{
  "conversation_id": 5,
  "message": "Add a task to buy groceries"
}
```

**Fields**:

- `conversation_id` (integer, optional): Existing conversation ID to continue.  
  - If omitted or null, a new conversation is created.
- `message` (string, required): User chat message (1–2000 characters).

## Response Schema *(mandatory)*

```json
{
  "conversation_id": 5,
  "response": "✓ I've added 'Buy groceries' to your task list.",
  "tool_calls": ["add_task"]
}
```

**Fields**:

- `conversation_id` (integer): The active conversation ID (new or existing).
- `response` (string): Assistant response shown to the user.
- `tool_calls` (array of strings): MCP tools invoked during processing.

## Conversation Handling *(mandatory)*

- If `conversation_id` is provided, the system loads the full message history for that conversation.
- If `conversation_id` is missing or null, the system creates a new conversation for the user.
- The system MUST store both the user message and assistant response as messages linked to the conversation.
- The system MUST allow the user to resume a prior conversation using the same `conversation_id`.

## Stateless Request Lifecycle *(mandatory)*

1. Receive the POST request with `user_id`, `conversation_id`, and `message`.
2. Validate JWT and confirm `user_id` matches the token identity.
3. Load conversation history from the database (if any).
4. Persist the incoming user message to the database.
5. Invoke the AI agent with MCP tools using the loaded history.
6. Persist the assistant response to the database.
7. Return the response payload immediately after persistence.

**Stateless Requirement**: No in-memory session state may be retained between requests. All conversational context must be reconstructed from the database on each request.

## Error Handling Expectations *(mandatory)*

- If authentication fails, return an authentication error response.
- If the `user_id` does not match the token, return an authorization error response.
- If `conversation_id` is invalid or belongs to another user, return a not-found or unauthorized error.
- If the AI service is unavailable, return a friendly retry message without creating partial state.
