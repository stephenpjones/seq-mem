# MCP Tools Definition

## Tool: think

**Purpose**: Process a single thought and record it in the graph

**Parameters**:
- `thought` (string, required): The thought content
- `confidence` (number, required): Confidence level (0.0-1.0)

**Returns**:
```json
{
    "status": "continue|branch|complete",
    "message": "string",
    "current_node_id": "string",
    "requires_alternatives": "boolean"
}
```

**Logic**:
1. Create new node with thought and confidence
2. Add edge from current node (if exists)
3. Update current node pointer
4. If confidence < 0.6, return branch status
5. Otherwise return continue status

---

## Tool: select_path

**Purpose**: Choose from alternative thoughts at a branch point

**Parameters**:
- `alternatives` (array, required): List of alternative thoughts
  ```json
  [
      {"thought": "string", "confidence": "number"},
      ...
  ]
  ```
- `selected_index` (integer, required): Which alternative to select (0-based)

**Returns**:
```json
{
    "status": "success",
    "message": "string",
    "selected_thought": "string",
    "current_node_id": "string"
}
```

**Logic**:
1. Validate selected_index is within bounds
2. Create nodes for all alternatives
3. Mark selected node as selected=True
4. Add edges from parent to all alternatives
5. Update current node to selected alternative

---

## Tool: backtrack

**Purpose**: Return to the last high-confidence node in the current path

**Parameters**: None

**Returns**:
```json
{
    "status": "success|no_target",
    "message": "string",
    "backtracked_to": {
        "node_id": "string",
        "thought": "string",
        "confidence": "number"
    }
}
```

**Logic**:
1. Get current path from root to current node
2. Traverse backwards to find node with confidence >= 0.6
3. Update current node pointer
4. Return node information

---

## Tool: show_current_path

**Purpose**: Display the current thinking path

**Parameters**: None

**Returns**:
```json
{
    "path": [
        {
            "node_id": "string",
            "thought": "string",
            "confidence": "number",
            "branch_point": "boolean"
        },
        ...
    ],
    "total_nodes": "integer",
    "branch_points": "integer"
}
```

**Logic**:
1. Get path from root to current node
2. Collect node information for each node in path
3. Count total branch points
4. Format and return

---

## Tool: get_unexplored_branches

**Purpose**: Find branch points with unexplored alternatives

**Parameters**: None

**Returns**:
```json
{
    "unexplored": [
        {
            "branch_node_id": "string",
            "branch_thought": "string",
            "unexplored_count": "integer",
            "alternatives": [
                {
                    "node_id": "string",
                    "thought": "string",
                    "confidence": "number"
                }
            ]
        }
    ]
}
```

**Logic**:
1. Find all nodes marked as branch_point=True
2. For each branch point, find unselected children
3. Return information about unexplored paths
