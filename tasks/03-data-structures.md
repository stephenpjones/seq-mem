# Data Structures

## Graph Schema

### Node Structure

```python
{
    "id": str,              # Unique identifier (e.g., "node_001")
    "thought": str,         # The actual thought content
    "confidence": float,    # Confidence level (0.0 - 1.0)
    "parent": str | None,   # Parent node ID
    "created_at": str,      # ISO timestamp
    "selected": bool,       # Was this node selected (vs alternative)
    "branch_point": bool    # Is this a branching decision point
}
```

### Edge Structure

```python
{
    "from": str,    # Source node ID
    "to": str,      # Target node ID
    "selected": bool # Was this the chosen path
}
```

### Graph State

```python
class ThoughtGraph:
    def __init__(self):
        self.nodes = {}          # Dict[str, Node]
        self.edges = []          # List[Edge]
        self.current_node = None # Current position
        self.node_counter = 0    # For generating IDs
```

## Example Graph State

```python
{
    "nodes": {
        "node_001": {
            "id": "node_001",
            "thought": "Let's start by understanding the problem",
            "confidence": 0.9,
            "parent": None,
            "created_at": "2024-01-01T10:00:00Z",
            "selected": True,
            "branch_point": False
        },
        "node_002": {
            "id": "node_002",
            "thought": "We need to consider multiple approaches",
            "confidence": 0.4,
            "parent": "node_001",
            "created_at": "2024-01-01T10:00:05Z",
            "selected": True,
            "branch_point": True
        },
        "node_003": {
            "id": "node_003",
            "thought": "Approach 1: Start with data structures",
            "confidence": 0.7,
            "parent": "node_002",
            "created_at": "2024-01-01T10:00:10Z",
            "selected": True,
            "branch_point": False
        },
        "node_004": {
            "id": "node_004",
            "thought": "Approach 2: Begin with architecture",
            "confidence": 0.6,
            "parent": "node_002",
            "created_at": "2024-01-01T10:00:10Z",
            "selected": False,
            "branch_point": False
        }
    },
    "edges": [
        {"from": "node_001", "to": "node_002", "selected": True},
        {"from": "node_002", "to": "node_003", "selected": True},
        {"from": "node_002", "to": "node_004", "selected": False}
    ],
    "current_node": "node_003",
    "node_counter": 4
}
```

## Path Representation

Current path from root to current node:
```python
["node_001", "node_002", "node_003"]
```

## Confidence Thresholds

- **High confidence**: >= 0.6
- **Low confidence**: < 0.6
- **Branch trigger**: When confidence < 0.6
