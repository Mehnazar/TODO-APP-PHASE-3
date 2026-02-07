---
id: 003
title: MCP tools spec
stage: spec
date: 2026-02-07
surface: agent
model: gpt-5.2-codex
feature: phase3-chatbot
branch: 001-phase3-chatbot
user: Mehnazar
command: Create @specs/api/mcp-tools.md for Phase III.
labels: ["phase-iii","mcp-tools","spec"]
links:
  spec: specs/api/mcp-tools.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/api/mcp-tools.md
tests:
 - none
---

## Prompt

<open_and_recently_viewed_files>
Recently viewed files (recent at the top, oldest at the bottom):
- c:\Users\Wajiz.pk\Documents\GitHub\hackathon-2-TODO-App\specs\001-phase3-chatbot\checklists\requirements.md (total lines: 35)

Files that are currently open and visible in the user's IDE:
- c:\Users\Wajiz.pk\Documents\GitHub\hackathon-2-TODO-App\specs\001-phase3-chatbot\checklists\requirements.md (currently focused file, cursor is on line 1, total lines: 35)

Note: these files may or may not be relevant to the current conversation. Use the read file tool if you need to get the contents of some of them.
</open_and_recently_viewed_files><user_query>
Create @specs/api/mcp-tools.md for Phase III.

Define MCP tools exposed by the MCP server:
- add_task
- list_tasks
- update_task
- complete_task
- delete_task

For each tool include:
- Purpose
- Parameters (with types and required fields)
- Return values
- Example input and output

Tools must be stateless and persist data using the database.
Do not write implementation code.

</user_query>

## Response snapshot

Created `specs/api/mcp-tools.md` defining all five MCP tools with purpose, parameters, return values, and examples, noting stateless and database persistence constraints.

## Outcome

- ✅ Impact: MCP tools spec drafted for Phase III.
- 🧪 Tests: none
- 📁 Files: specs/api/mcp-tools.md
- 🔁 Next prompts: Generate plan with `/sp.plan` if needed.
- 🧠 Reflection: Keep tool definitions precise and consistent across commands.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): none
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): none
