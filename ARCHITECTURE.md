# Architecture Overview

## System Design

This document describes the architecture of the Agentic Workflow Framework.

```
┌─────────────────────────────────────────────────────────────┐
│                      USER INTERFACE                          │
│              (Task/Goal from User)                          │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    AGENT CORE                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Agent.run(task) - Main Orchestrator               │   │
│  │  - Manages agent lifecycle                          │   │
│  │  - Coordinates components                           │   │
│  │  - Implements decision loop                         │   │
│  └──────────────────────────────────────────────────────┘   │
└──────────────┬──────────────┬──────────────┬────────────────┘
               │              │              │
        ┌──────▼──┐    ┌──────▼──┐   ┌──────▼──┐
        │   LLM   │    │  TOOLS  │   │ MEMORY  │
        │ CLIENT  │    │REGISTRY │   │         │
        └─────────┘    └─────────┘   └─────────┘
```

## Components

### 1. Agent (src/agent.py)
**Responsibility**: Main orchestrator of the workflow

**Key Methods**:
- `run(task)`: Execute a task from start to finish
- `_get_llm_response()`: Get next action from LLM
- `_process_tool_call()`: Execute tools requested by LLM
- `register_tool()`: Register custom tools

**Decision Loop**:
```
1. User provides task
2. Agent sends to LLM with available tools
3. LLM decides:
   - Use tool(s) → Execute and loop
   - No tool needed → Return final response
4. Repeat until task complete or max iterations
```

### 2. LLM Client (src/llm_client.py)
**Responsibility**: Interface with OpenAI API

**Key Features**:
- Manages API communication
- Handles conversation history
- Supports tool/function calling
- Error handling and retries

**Methods**:
- `call()`: Send messages to LLM
- `add_to_history()`: Track conversation
- `clear_history()`: Reset context

### 3. Tools Registry (src/tools.py)
**Responsibility**: Manage available tools/functions

**Tool Categories**:
- **Math**: `calculate` - Mathematical expressions
- **Text**: `string_analysis` - Text analysis
- **Data**: `list_operations` - List operations
- **Time**: `get_current_time` - Timestamps
- **Code**: `code_analyzer` - Code analysis

**Methods**:
- `register()`: Add new tool
- `execute()`: Run tool with parameters
- `list_tools()`: Get all tools in OpenAI format
- `to_openai_format()`: Convert to API format

### 4. Memory (src/memory.py)
**Responsibility**: Store context and execution history

**Stored Data**:
- **Messages**: Complete conversation history
- **Task Context**: Goal, status, metadata
- **Tool Results**: What tools returned
- **Decisions**: Agent decisions and reasoning

**Methods**:
- `add_message()`: Store conversation
- `add_tool_result()`: Record tool execution
- `get_messages()`: Retrieve for LLM
- `export()`: Save entire session

## Information Flow

### Task Execution Flow

```
1. INITIALIZE
   ├─ Clear memory
   ├─ Set task context
   └─ Add system message

2. MAIN LOOP (up to max_iterations)
   ├─ Get LLM response
   │  ├─ Send: Messages + Available tools
   │  └─ Receive: Content + Tool calls + Finish reason
   │
   ├─ Check finish reason
   │  ├─ "stop" → Task complete, return response
   │  └─ "tool_calls" → Process tools
   │
   └─ Process tool calls
      ├─ Parse tool name and parameters
      ├─ Execute tool
      ├─ Store result in memory
      └─ Loop again

3. FINALIZE
   ├─ Update task context
   └─ Return final result
```

## Message Format

### System Message
Contains:
- Agent name and purpose
- Available tools
- Instructions for behavior

### Conversation
```
[System] → Instructions
[User]   → Task description
[Assistant] → Analysis + tool calls
[User]   → Tool results
[Assistant] → Next analysis
...
[Assistant] → Final answer
```

## Tool Definition Format

```python
{
    "type": "function",
    "function": {
        "name": "tool_name",
        "description": "What the tool does",
        "parameters": {
            "type": "object",
            "properties": {
                "param1": {"type": "string", "description": "..."},
                "param2": {"type": "integer", "description": "..."}
            },
            "required": ["param1", "param2"]
        }
    }
}
```

## Error Handling

### Tool Execution Errors
- Caught and logged
- Error message sent back to agent
- Agent can retry or adapt strategy

### LLM Errors
- API errors handled gracefully
- Logged with context
- Agent loop terminates

### Invalid Parameters
- Tool validates input
- Returns error message
- Agent receives feedback

## Extensibility

### Adding Custom Tools

```python
agent = Agent()

agent.register_tool(
    name="my_tool",
    description="Does something special",
    func=my_function,
    parameters={
        "type": "object",
        "properties": {...}
    }
)
```

### Custom Agents

Inherit from Agent and override:
- `_build_system_message()`: Custom instructions
- `_get_llm_response()`: Custom LLM logic
- `_process_tool_call()`: Custom execution

## Performance Considerations

1. **Token Usage**
   - Longer context = more tokens
   - Memory keeps conversation focused
   - Consider summarization for long sessions

2. **API Costs**
   - Each LLM call costs money
   - Use appropriate temperature
   - Limit iterations

3. **Tool Execution**
   - Tools should complete quickly
   - Consider timeout policies
   - Cache frequently used results

## Security Considerations

1. **Code Execution**
   - `calculate` uses restricted eval
   - `code_analyzer` doesn't execute user code
   - External tools need authentication

2. **API Keys**
   - Use environment variables
   - Never commit .env
   - Rotate keys regularly

3. **Tool Permissions**
   - Validate all inputs
   - Implement rate limiting
   - Audit tool usage

## Future Enhancements

- [ ] Multi-agent coordination
- [ ] Long-term memory persistence
- [ ] Knowledge base integration
- [ ] Advanced planning algorithms
- [ ] Parallel tool execution
- [ ] Tool result caching
- [ ] Cost optimization
- [ ] Monitoring and observability
