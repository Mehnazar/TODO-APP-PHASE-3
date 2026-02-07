# Tasks: Phase III Todo AI Chatbot

**Input**: Design documents from `/specs/001-phase3-chatbot/`  
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/  
**Tests**: Not requested in spec (no test tasks included)

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create MCP module structure in `backend/src/mcp/` and update `backend/src/__init__.py`
- [x] T002 [P] Add MCP server configuration placeholders to `backend/src/config.py`
- [x] T003 [P] Document MCP-related env vars in `backend/.env.example`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

- [x] T004 Extend `backend/src/models.py` with Conversation and Message models (SQLModel)
- [x] T005 Create Alembic migration file for conversations/messages in `backend/alembic/versions/`
- [x] T006 [P] Add database access helpers for chat history in `backend/src/services/`
- [x] T007 [P] Add standardized MCP tool response helpers in `backend/src/utils/`
- [x] T008 Wire MCP server startup into `backend/src/main.py`

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Chat-Based Task CRUD (Priority: P1) 🎯 MVP

**Goal**: Natural language chat can create/list/update/complete/delete tasks with confirmations.

**Independent Test**: Send chat requests that map to CRUD actions and verify task changes and confirmations.

### Implementation for User Story 1

- [x] T009 [P] Implement MCP tool: add_task in `backend/src/mcp/tools.py`
- [x] T010 [P] Implement MCP tool: list_tasks in `backend/src/mcp/tools.py`
- [x] T011 [P] Implement MCP tool: update_task in `backend/src/mcp/tools.py`
- [x] T012 [P] Implement MCP tool: complete_task in `backend/src/mcp/tools.py`
- [x] T013 [P] Implement MCP tool: delete_task in `backend/src/mcp/tools.py`
- [x] T014 Implement MCP server wiring in `backend/src/mcp/server.py`
- [x] T015 Implement chat endpoint handler in `backend/src/routes/chat.py`
- [x] T016 Add agent orchestration using OpenAI Agents SDK in `backend/src/services/agent_service.py`

**Checkpoint**: User Story 1 functional and testable independently

---

## Phase 4: User Story 2 - Authenticated Chat Access (Priority: P2)

**Goal**: Chat access requires JWT and enforces user isolation.

**Independent Test**: Unauthorized requests are rejected; user_id mismatch denied.

### Implementation for User Story 2

- [x] T017 Add JWT guard and user_id checks in `backend/src/routes/chat.py`
- [x] T018 Enforce user isolation in MCP tools in `backend/src/mcp/tools.py`

**Checkpoint**: Authenticated access enforced for chat and tools

---

## Phase 5: User Story 3 - Persistent Conversation History (Priority: P3)

**Goal**: Conversation history persists and can be resumed across sessions.

**Independent Test**: Resume a conversation by ID and verify history is used.

### Implementation for User Story 3

- [x] T019 Add conversation create/load helpers in `backend/src/services/chat_history_service.py`
- [x] T020 Persist user/assistant messages in `backend/src/services/chat_history_service.py`
- [x] T021 Update chat endpoint to load history and save messages in `backend/src/routes/chat.py`

**Checkpoint**: Conversation history persisted and reusable

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T022 [P] Update API documentation in `specs/api/` if needed for final alignment
- [x] T023 Add logging for chat and tool execution in `backend/src/services/`
- [ ] T024 Run quickstart.md validation scenarios manually

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies
- **Foundational (Phase 2)**: Depends on Setup completion
- **User Stories (Phase 3+)**: Depend on Foundational completion
- **Polish (Phase 6)**: Depends on desired user stories complete

### User Story Dependencies

- **User Story 1 (P1)**: Starts after Foundational; no dependency on other stories
- **User Story 2 (P2)**: Starts after Foundational; integrates with US1 endpoints/tools
- **User Story 3 (P3)**: Starts after Foundational; integrates with chat endpoint and DB models

### Parallel Opportunities

- MCP tools T009–T013 can run in parallel
- Foundational tasks T006–T007 can run in parallel

