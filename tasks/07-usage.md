# Usage Guide

## Installation

1. Clone the repository:
   ```bash
   git clone [repository-url]
   cd seq-mem
   ```

2. Install dependencies:
   ```bash
   pip install mcp
   ```

3. Add to Claude Desktop MCP configuration:
   ```json
   {
     "mcpServers": {
       "sequential-memory": {
         "command": "python",
         "args": ["-m", "sequential_memory.server"],
         "cwd": "C:\\Users\\steve\\claude\\seq-mem\\src"
       }
     }
   }
   ```

4. Restart Claude Desktop

## Basic Usage

### Starting a Thinking Session

```
User: Let's use sequential thinking to solve [problem]

Claude: I'll help you solve this step by step using sequential thinking.

[Uses think tool]: "First, let me understand the problem clearly" (confidence: 0.8)

[Uses think tool]: "The key aspects seem to be..." (confidence: 0.9)

[Uses think tool]: "Now I need to consider different approaches..." (confidence: 0.4)

I've reached a point of uncertainty. Let me generate several alternative paths to explore:

[Uses select_path tool with 5 alternatives]
```

### Exploring Branches

When confidence drops below 0.6, Claude will automatically generate alternatives:

```
Claude: I'm not confident about the next step. Here are 5 possible directions:

1. "We could start by analyzing the data structure" (0.7)
2. "Let's focus on the user interface first" (0.6)
3. "Perhaps we should define the API endpoints" (0.8)
4. "We might want to consider security implications" (0.5)
5. "Let's think about scalability requirements" (0.6)

[Selects option 3 - highest confidence]

Continuing with: "Perhaps we should define the API endpoints"
```

### Backtracking

When a path doesn't lead to a good solution:

```
User: This approach isn't working. Let's backtrack.

Claude: [Uses backtrack tool]

I've backtracked to: "Now I need to consider different approaches..." 

From here, we previously explored "API endpoints first". We have these unexplored alternatives:
- "We could start by analyzing the data structure" (0.7)
- "Let's focus on the user interface first" (0.6)
- "We might want to consider security implications" (0.5)
- "Let's think about scalability requirements" (0.6)

Which would you like to explore?
```

### Viewing the Current Path

```
User: Show me our thinking path so far

Claude: [Uses show_current_path tool]

Current thinking path:
1. "First, let me understand the problem clearly" (0.8)
2. "The key aspects seem to be..." (0.9)
3. "Now I need to consider different approaches..." (0.4) [BRANCH POINT]
4. "Perhaps we should define the API endpoints" (0.8)
5. "We need RESTful design" (0.7)
6. "Consider authentication method" (0.5) [BRANCH POINT]
7. "Use JWT tokens" (0.8)

Total nodes: 7
Branch points: 2
```

## Example Scenarios

### Scenario 1: Problem Solving
```
User: Help me figure out how to optimize my website's performance

Claude: I'll help you think through website optimization systematically.

[Thinks]: "First, we need to identify the performance bottlenecks" (0.9)
[Thinks]: "Let's analyze the current metrics" (0.8)
[Thinks]: "There are several areas to consider..." (0.3)

[Branches into]: 
- Frontend optimization
- Backend optimization  
- Database optimization
- CDN and caching
- Infrastructure scaling
```

### Scenario 2: Creative Writing
```
User: Let's brainstorm plot directions for my story

Claude: Let's explore different narrative paths for your story.

[Thinks]: "The protagonist has just discovered the truth" (0.9)
[Thinks]: "They need to make a choice" (0.7)
[Thinks]: "Several possibilities emerge..." (0.4)

[Branches into]:
- Confront the antagonist immediately
- Gather allies first
- Investigate further
- Try to escape
- Attempt reconciliation
```

## Tips for Effective Use

1. **Encourage branching**: When you sense uncertainty, you can explicitly ask for alternatives

2. **Use backtracking strategically**: Don't abandon a path too quickly, but don't hesitate to backtrack when truly stuck

3. **Explore multiple paths**: The tool is designed to map out decision spaces, not just find one solution

4. **Review unexplored branches**: Before concluding, check what alternatives you haven't explored

5. **Confidence calibration**: Pay attention to confidence scores - they indicate where thinking is solid vs uncertain

## Common Commands

- "Let's think about this step by step" - Initiates sequential thinking
- "I'm not sure about this approach" - May trigger branching
- "Let's backtrack and try another way" - Returns to previous decision point
- "Show me our thinking path" - Displays current path
- "What haven't we explored?" - Shows unexplored branches
- "Let's try the alternative approach" - Selects different branch
