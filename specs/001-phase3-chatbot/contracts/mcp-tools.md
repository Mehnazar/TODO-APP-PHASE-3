# Contract: MCP Tools

**Source Spec**: `specs/api/mcp-tools.md`

## Tools

- `add_task`
- `list_tasks`
- `update_task`
- `complete_task`
- `delete_task`

## Notes

- All tools are stateless and must persist data via SQLModel.
- `user_id` is the first parameter for all tools.

