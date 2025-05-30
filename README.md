# Sequential-Memory MCP Server

Sequential-Memory is a Model Context Protocol (MCP) server that combines sequential thinking with persistent memory through a knowledge graph. It enables AI assistants to explore decision trees by recording thinking traces, branching at low-confidence points, and backtracking to explore alternative paths.

## Core Concept

1. **Linear thinking** when confidence is high
2. **Branching** when confidence drops below threshold
3. **Path recording** in an in-memory graph
4. **Backtracking** to explore alternative branches
5. **Path visualization** to see thinking traces

## Technology Stack

- Python 3.10+
- MCP Python SDK
- In-memory graph (dictionaries)
- Claude Desktop (client)

## Project Scope

This is a minimal prototype focusing on:
- Core thinking/branching mechanism
- Simple confidence-based decisions
- Basic backtracking
- Path recording and viewing

Not included (yet):
- Persistent storage
- Complex metrics
- Visualization beyond text
- Pattern recognition
- Multi-agent exploration

## Directory Structure

```
seq-mem/
├── tasks/                  (task breakdown and planning)
├── src/                    (source code)
├── tests/                  (test files)
└── README.md              (this file)
```

For detailed implementation plans and task breakdown, see the `tasks/` directory starting with `00-overview.md`.
