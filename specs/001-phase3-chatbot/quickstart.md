# Phase 1 Quickstart: Phase III Todo AI Chatbot

**Date**: 2026-02-07  
**Branch**: `001-phase3-chatbot`

## Scenario 1: Create and List Tasks via Chat

1. Authenticate and obtain JWT.
2. Send `POST /api/{user_id}/chat` with message: "Add a task to buy groceries".
3. Expect confirmation response and a `tool_calls` list containing `add_task`.
4. Send `POST /api/{user_id}/chat` with message: "What's on my list?"
5. Expect a list of tasks in the response.

## Scenario 2: Complete and Delete Tasks via Chat

1. Send `POST /api/{user_id}/chat` with message: "Mark task 1 as done".
2. Expect confirmation with `complete_task`.
3. Send `POST /api/{user_id}/chat` with message: "Delete task 1".
4. Expect confirmation with `delete_task`.

## Scenario 3: Resume Conversation

1. Send a chat message with `conversation_id` set to an existing conversation.
2. Expect the assistant to respond based on prior history.

