# Database Schema Specification (Phase III Update)

**Project**: Evolution of Todo  
**Database**: Neon Serverless PostgreSQL  
**ORM**: SQLModel (SQLAlchemy + Pydantic)  
**Version**: 1.1.0  
**Created**: 2025-12-25  
**Last Updated**: 2026-02-07  

---

## Overview

PostgreSQL schema for Evolution of Todo covering Phase II (authentication and tasks) and Phase III (conversations and messages). Conversation state is stored in the database and reconstructed per request.

## Design Principles

1. **UTC Timestamps** - All datetime fields store UTC
2. **VARCHAR for User IDs** - Better Auth generates string IDs (format: `usr_xxxxx`)
3. **SERIAL for Task/Conversation/Message IDs** - Auto-increment integers
4. **Foreign Keys** - Enforce referential integrity at database level
5. **Indexes** - On frequently queried columns (user_id, email, completed, created_at)
6. **No In-Memory State** - All conversation state persisted in DB

---

## Phase II: Users and Tasks (Reference)

### users

**Purpose:** Store user accounts (Better Auth integration)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | VARCHAR(255) | PRIMARY KEY | User ID from Better Auth |
| email | VARCHAR(255) | UNIQUE, NOT NULL | User email address |
| name | VARCHAR(255) | NULL | User display name |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() AT TIME ZONE 'UTC' | Account creation time (UTC) |

**Indexes:**
- PRIMARY KEY on `id`
- UNIQUE INDEX on `email`

---

### tasks

**Purpose:** Store user tasks with completion status

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | SERIAL | PRIMARY KEY | Auto-increment task ID |
| user_id | VARCHAR(255) | NOT NULL, FOREIGN KEY → users(id) | Task owner |
| title | VARCHAR(200) | NOT NULL | Task title |
| description | VARCHAR(1000) | NOT NULL, DEFAULT '' | Task description |
| completed | BOOLEAN | NOT NULL, DEFAULT FALSE | Completion status |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() AT TIME ZONE 'UTC' | Task creation time (UTC) |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() AT TIME ZONE 'UTC' | Last update time (UTC) |

**Indexes:**
- PRIMARY KEY on `id`
- INDEX on `user_id`
- INDEX on `completed`
- INDEX on `created_at`

---

## Phase III: Conversations and Messages

### conversations

**Purpose:** Store chat conversations for each user (stateless reconstruction).

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | SERIAL | PRIMARY KEY | Auto-increment conversation ID |
| user_id | VARCHAR(255) | NOT NULL, FOREIGN KEY → users(id) | Conversation owner |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() AT TIME ZONE 'UTC' | Conversation start time (UTC) |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() AT TIME ZONE 'UTC' | Last message time (UTC) |

**Relationships:**
- `conversations.user_id` → `users.id` (ON DELETE CASCADE)
- `messages.conversation_id` → `conversations.id` (ON DELETE CASCADE)

**Indexes:**
- PRIMARY KEY on `id`
- INDEX on `user_id` (list user conversations)
- INDEX on `updated_at` (sort by recent activity)

---

### messages

**Purpose:** Store individual messages within conversations.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | SERIAL | PRIMARY KEY | Auto-increment message ID |
| conversation_id | INTEGER | NOT NULL, FOREIGN KEY → conversations(id) | Parent conversation |
| user_id | VARCHAR(255) | NOT NULL, FOREIGN KEY → users(id) | Message owner (same as conversation owner) |
| role | VARCHAR(20) | NOT NULL | 'user' or 'assistant' |
| content | TEXT | NOT NULL | Message text content |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() AT TIME ZONE 'UTC' | Message timestamp (UTC) |

**Relationships:**
- `messages.conversation_id` → `conversations.id` (ON DELETE CASCADE)
- `messages.user_id` → `users.id` (ON DELETE CASCADE)

**Indexes:**
- PRIMARY KEY on `id`
- INDEX on `conversation_id` (load messages by conversation)
- INDEX on `created_at` (chronological ordering)

**Notes:**
- Conversation state must be loaded from these tables each request.
- No in-memory session state is allowed.

---

## Acceptance Criteria

- [x] Conversations table schema defined with fields, types, relationships, and indexes
- [x] Messages table schema defined with fields, types, relationships, and indexes
- [x] Conversation state persisted in DB (no in-memory state)

