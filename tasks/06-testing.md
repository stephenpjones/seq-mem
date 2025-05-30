# Testing Plan

## Unit Tests

### Graph Module Tests

**test_node_creation**
- Create node with all fields
- Verify ID generation
- Check timestamp format

**test_edge_creation**
- Create edge between nodes
- Verify from/to references
- Check selected flag

**test_path_retrieval**
- Build multi-node graph
- Get path from root to leaf
- Verify correct ordering

**test_backtrack_finding**
- Create path with mixed confidence
- Find last high-confidence node
- Handle no high-confidence case

### Tools Module Tests

**test_think_high_confidence**
- Call think with confidence > 0.6
- Verify continue status
- Check node creation

**test_think_low_confidence**
- Call think with confidence < 0.6
- Verify branch status
- Check requires_alternatives flag

**test_select_path_valid**
- Provide alternatives array
- Select valid index
- Verify correct node marked selected

**test_select_path_invalid**
- Test out-of-bounds index
- Test empty alternatives
- Verify error handling

## Integration Tests

### Scenario 1: Linear Thinking
```python
# All thoughts have high confidence
# No branching occurs
# Path should be straight line
```

### Scenario 2: Single Branch
```python
# Start with high confidence
# Drop to low confidence once
# Select from alternatives
# Continue with high confidence
```

### Scenario 3: Multiple Branches
```python
# Multiple low-confidence points
# Different selections at each
# Verify graph structure
```

### Scenario 4: Backtrack and Explore
```python
# Create path with branches
# Backtrack to branch point
# Explore different alternative
# Verify both paths exist
```

## End-to-End Test Scenarios

### Problem-Solving Session
```
1. "Let's solve how to implement a feature" (0.8)
2. "First, understand requirements" (0.9)
3. "Then we need to..." (0.3) → BRANCH
4. Alternatives:
   - "Design the API first" (0.7)
   - "Create data models" (0.6)
   - "Build UI prototype" (0.5)
5. Select option 0 (API first)
6. "Define endpoints" (0.8)
7. "Consider REST vs GraphQL" (0.4) → BRANCH
8. Backtrack to step 4
9. Select option 1 (data models)
10. Show final path
```

### Expected Outcomes
- Graph contains 2 explored paths
- 1 unexplored branch at step 4
- Backtrack correctly returns to step 4
- Path display shows actual route taken

## Error Handling Tests

### Invalid Inputs
- Confidence outside 0-1 range
- Missing required parameters
- Wrong parameter types
- Empty thought content

### State Errors
- Backtrack with no path
- Select path without prior branch
- Get path with empty graph

## Performance Tests

### Large Graph
- Create 100+ nodes
- Multiple branch points
- Verify operations stay responsive
- Check memory usage reasonable

## Manual Testing Checklist

- [ ] Install in Claude Desktop
- [ ] Basic think operation works
- [ ] Branching triggers at low confidence
- [ ] Can select from alternatives
- [ ] Backtrack finds correct node
- [ ] Path display is readable
- [ ] Unexplored branches shown correctly
- [ ] Error messages are helpful
- [ ] No crashes during normal use
- [ ] State persists across tool calls
