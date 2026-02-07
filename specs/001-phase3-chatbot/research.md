# Phase 0 Research: Phase III Todo AI Chatbot

**Date**: 2026-02-07  
**Branch**: `001-phase3-chatbot`

## Decisions

### 1) Conversation state storage

- **Decision**: Persist conversation and message history in Neon PostgreSQL and reconstruct per request.
- **Rationale**: Aligns with Phase III specs for stateless architecture and existing Neon infrastructure.
- **Alternatives considered**: Dapr State API (deferred to Phase V due to infrastructure scope).

### 2) Agent runtime

- **Decision**: Use OpenAI Agents SDK for intent interpretation and tool orchestration.
- **Rationale**: Required by Phase III constraints and provides structured tool calling.
- **Alternatives considered**: Custom LLM routing (not allowed by spec).

### 3) Tool interface

- **Decision**: Implement MCP tools via official MCP SDK with `user_id` as first parameter.
- **Rationale**: Matches MCP tool standards in constitution and Phase III specs.
- **Alternatives considered**: Direct REST calls (not compliant with MCP tool requirements).

