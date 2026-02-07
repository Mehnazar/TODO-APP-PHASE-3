# Phase 1 Data Model: Phase III Todo AI Chatbot

**Date**: 2026-02-07  
**Branch**: `001-phase3-chatbot`

## Entities

### User

- **Represents**: Authenticated account from Phase II
- **Key Attributes**: `id`, `email`, `name`, `created_at`
- **Relationships**: One-to-many with `Task`, `Conversation`, `Message`

### Task

- **Represents**: A single todo item
- **Key Attributes**: `id`, `user_id`, `title`, `description`, `completed`, `created_at`, `updated_at`
- **Relationships**: Many-to-one with `User`

### Conversation

- **Represents**: A chat session for a user
- **Key Attributes**: `id`, `user_id`, `created_at`, `updated_at`
- **Relationships**: Many-to-one with `User`, one-to-many with `Message`

### Message

- **Represents**: A single chat message in a conversation
- **Key Attributes**: `id`, `conversation_id`, `user_id`, `role`, `content`, `created_at`
- **Relationships**: Many-to-one with `Conversation`, many-to-one with `User`

## Validation Rules

- `user_id` must match authenticated identity
- `role` must be `user` or `assistant`
- `content` must be non-empty

