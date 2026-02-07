# Architecture Overview

**Project**: Evolution of Todo  
**Version**: 1.1.0  
**Last Updated**: 2026-02-07  

---

## Phase III: AI Chatbot Architecture

### Components

- **ChatKit Frontend**: User-facing chat interface for natural language task management.
- **FastAPI Backend**: Single stateless entrypoint for chat and task operations.
- **OpenAI Agents SDK**: Agent runtime that interprets user intent and orchestrates tool calls.
- **MCP Server**: Exposes MCP tools for task CRUD and conversation access.
- **Neon PostgreSQL**: Persistent storage for users, tasks, conversations, and messages.

### Stateless Request Flow

1. **User message** is sent from ChatKit to `POST /api/{user_id}/chat`.
2. **FastAPI validates JWT** via Better Auth and confirms `user_id` matches the token.
3. **Conversation history** is loaded from Neon PostgreSQL using `conversation_id` (if provided).
4. **User message** is persisted to Neon PostgreSQL.
5. **OpenAI Agent** runs with the MCP toolset and the retrieved history.
6. **MCP Server** executes task tools (add/list/update/complete/delete) using database persistence only.
7. **Assistant response** is persisted to Neon PostgreSQL.
8. **FastAPI returns** the response payload to ChatKit.

**Stateless Constraint**: No in-memory session state is retained between requests. All conversational context is reconstructed from the database on each call.

