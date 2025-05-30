# Sequential-Memory MCP Server

## Project Overview

Sequential-Memory is a Model Context Protocol (MCP) server that combines sequential thinking with persistent memory through a knowledge graph. It enables AI assistants to explore decision trees by recording thinking traces, branching at low-confidence points, and backtracking to explore alternative paths.

## Core Concept

1. **Linear thinking** when confidence is high
2. **Branching** when confidence drops below threshold
3. **Path recording** in an in-memory graph
4. **Backtracking** to explore alternative branches
5. **Path visualization** to see thinking traces

## Directory Structure

```
seq-mem/
├── 00-overview.md          (this file)
├── 01-setup.md            (environment and dependencies)
├── 02-architecture.md     (system design)
├── 03-data-structures.md  (graph schema)
├── 04-mcp-tools.md        (tool definitions)
├── 05-implementation.md   (step-by-step build plan)
├── 06-testing.md          (test scenarios)
└── 07-usage.md            (example interactions)
```

## Technology Stack

- Python 3.10+
- MCP Python SDK
- In-memory graph (dictionaries)
- Claude Desktop (client)

## Scope

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
