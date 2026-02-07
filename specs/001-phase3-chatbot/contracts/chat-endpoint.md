# Contract: POST /api/{user_id}/chat

**Source Spec**: `specs/api/chat-endpoint.md`

## Request Schema

```json
{
  "conversation_id": 5,
  "message": "Add a task to buy groceries"
}
```

## Response Schema

```json
{
  "conversation_id": 5,
  "response": "✓ I've added 'Buy groceries' to your task list.",
  "tool_calls": ["add_task"]
}
```

## Notes

- JWT required; `user_id` must match token identity.
- Stateless: history loaded from DB each request.

