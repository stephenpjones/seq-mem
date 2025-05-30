# Architecture Design

## System Components

### 1. MCP Server (server.py)
- Handles MCP protocol communication
- Manages server lifecycle
- Routes tool calls to appropriate handlers

### 2. Thought Graph (graph.py)
- In-memory graph storage
- Node and edge management
- Path traversal operations
- State tracking (current node)

### 3. Tools Module (tools.py)
- Tool definitions and handlers
- Input validation
- Response formatting

## Core Flow

```
Claude Desktop
    |
    v
MCP Server
    |
    ├─> think() ──────> Graph.add_thought()
    |                        |
    |                        v
    |                   Check confidence
    |                        |
    |                 ┌──────┴──────┐
    |                 |             |
    |           High (>0.6)    Low (<0.6)
    |                 |             |
    |                 v             v
    |           Continue      Request branches
    |                              |
    ├─> select_path() <───────────┘
    |       |
    |       v
    |   Graph.select_branch()
    |
    ├─> backtrack() ──> Graph.find_last_high_confidence()
    |
    └─> show_path() ──> Graph.get_current_path()
```

## State Management

The graph maintains:
- Current node ID
- All nodes (thoughts with metadata)
- All edges (connections between thoughts)
- Current path (list of node IDs from root)

## Error Handling

- Invalid tool parameters → Clear error message
- No high-confidence node for backtrack → Informative response
- Graph operations failures → Graceful degradation

## Concurrency

- Single-threaded for prototype
- All operations are synchronous
- State mutations are atomic at the tool level
