# Sequential Memory MCP Server

A Model Context Protocol (MCP) server that combines sequential thinking with persistent memory through a knowledge graph. This enables AI assistants to explore decision trees by recording thinking traces, branching at low-confidence points, and backtracking to explore alternative paths.

## Features

- **Linear thinking** when confidence is high (≥ 0.6)
- **Automatic branching** when confidence drops below threshold (< 0.6)
- **Path recording** in an in-memory graph structure
- **Backtracking** to explore alternative branches
- **Path visualization** to see complete thinking traces
- **Unexplored branch detection** to identify paths not yet taken

## Installation

1. Clone this repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   # or
   source venv/bin/activate  # On Unix/MacOS
   ```
3. Install dependencies:
   ```bash
   pip install mcp
   ```

## Configuration

Add the following to your Claude Desktop configuration file:
`C:\Users\steve\AppData\Roaming\Claude\claude_desktop_config.json`

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

## Usage

The server provides 5 main tools:

### 1. think
Process a thought with a confidence level.
- **Parameters**: 
  - `thought` (string): The thought content
  - `confidence` (number): Confidence level (0.0-1.0)
- **Returns**: Status (continue/branch), current node ID, and whether alternatives are needed

### 2. select_path
Choose from alternative thoughts at a branch point.
- **Parameters**:
  - `alternatives` (array): List of alternative thoughts with confidence levels
  - `selected_index` (integer): Which alternative to select (0-based)
- **Returns**: Selected thought information and new current node ID

### 3. backtrack
Return to the last high-confidence node in the current path.
- **Parameters**: None
- **Returns**: Information about the node backtracked to (or no_target if none found)

### 4. show_current_path
Display the current thinking path from root to current node.
- **Parameters**: None
- **Returns**: Complete path with node details, total nodes, and branch points

### 5. get_unexplored_branches
Find all branch points with unexplored alternatives.
- **Parameters**: None
- **Returns**: List of unexplored branches with their alternatives

## Example Usage

```
User: Let's think through a problem step by step.

Claude: I'll use sequential thinking to explore this systematically.

[thinks: "First, let me understand the problem clearly" (0.8)]
[thinks: "The key aspects seem to be X, Y, and Z" (0.9)]
[thinks: "Now I need to decide on an approach..." (0.3)]

I've reached a point of uncertainty. Let me explore different approaches:

[select_path with alternatives:
  - "Focus on aspect X first" (0.7)
  - "Start with aspect Y" (0.6)
  - "Consider aspect Z" (0.5)]

[Continue thinking on selected path...]

User: Let's backtrack and try a different approach.

Claude: [backtrack]
I've returned to "The key aspects seem to be X, Y, and Z". 
Let me explore one of the other approaches...
```

## Testing

Run the test suite:
```bash
python -m pytest tests/test_basic.py
# or
python tests/test_basic.py
```

## Architecture

- **graph.py**: Core graph data structures (Node, Edge, ThoughtGraph)
- **tools.py**: MCP tool implementations and definitions
- **server.py**: Main MCP server implementation
- **test_basic.py**: Comprehensive test suite

## Development

The codebase is organized for clarity and extensibility:
- All graph operations are encapsulated in the `ThoughtGraph` class
- Tool handlers are separated in the `SequentialMemoryTools` class
- The server handles only MCP protocol communication
- Tests cover both unit and integration scenarios
