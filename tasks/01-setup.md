# Setup and Environment

## Prerequisites

- Python 3.10 or higher
- pip package manager
- Claude Desktop application

## Python Dependencies

```bash
# Core MCP SDK
mcp

# Standard library only for prototype
# No additional dependencies needed
```

## Project Structure

```
seq-mem/
├── pyproject.toml         # Project configuration
├── src/
│   └── sequential_memory/
│       ├── __init__.py
│       ├── server.py      # Main MCP server
│       ├── graph.py       # In-memory graph implementation
│       └── tools.py       # MCP tool definitions
└── tests/
    └── test_basic.py      # Basic functionality tests
```

## Development Setup

1. Create virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate virtual environment:
   ```bash
   # Windows
   venv\Scripts\activate
   
   # Unix/MacOS
   source venv/bin/activate
   ```

3. Install MCP SDK:
   ```bash
   pip install mcp
   ```

## Claude Desktop Configuration

Add to MCP settings in Claude Desktop:
config file location: "C:\Users\steve\AppData\Roaming\Claude\claude_desktop_config.json"

```json
{
  "mcpServers": {
    "sequential-memory": {
      "command": "python",
      "args": [
        "-m",
        "sequential_memory.server"
      ],
      "cwd": "C:\\Users\\steve\\claude\\seq-mem\\src"
    }
  }
}
```

## Environment Variables

No environment variables required for basic prototype.
