"""MCP tool definitions and handlers for sequential memory."""

from typing import Dict, List, Optional, Any
from .graph import ThoughtGraph, Node


class SequentialMemoryTools:
    """Handles all tool operations for sequential memory."""
    
    def __init__(self):
        """Initialize with an empty thought graph."""
        self.graph = ThoughtGraph()
    
    def think(self, thought: str, confidence: float) -> dict:
        """
        Process a single thought and record it in the graph.
        
        Args:
            thought: The thought content
            confidence: Confidence level (0.0-1.0)
            
        Returns:
            Status and information about the thought processing
        """
        # Validate confidence
        if not 0.0 <= confidence <= 1.0:
            raise ValueError("Confidence must be between 0.0 and 1.0")
        
        # Add the thought node
        node = self.graph.add_node(
            thought=thought,
            confidence=confidence,
            parent=self.graph.current_node
        )
        
        # Determine status based on confidence
        if confidence < 0.6:
            status = "branch"
            requires_alternatives = True
            message = f"Low confidence ({confidence}). Please provide alternative thoughts to explore."
        else:
            status = "continue"
            requires_alternatives = False
            message = f"Thought recorded with confidence {confidence}. Continue thinking."
        
        return {
            "status": status,
            "message": message,
            "current_node_id": node.id,
            "requires_alternatives": requires_alternatives
        }
    
    def select_path(self, alternatives: List[Dict[str, Any]], 
                    selected_index: int) -> dict:
        """
        Choose from alternative thoughts at a branch point.
        
        Args:
            alternatives: List of alternative thoughts with confidence
            selected_index: Which alternative to select (0-based)
            
        Returns:
            Information about the selected path
        """
        # Validate inputs
        if not alternatives:
            raise ValueError("Alternatives list cannot be empty")
        
        if not 0 <= selected_index < len(alternatives):
            raise ValueError(f"Selected index {selected_index} out of range")
        
        # Create branch alternatives
        selected_node = self.graph.create_branch_alternatives(
            alternatives, selected_index
        )
        
        if not selected_node:
            raise RuntimeError("Failed to create branch alternatives")
        
        return {
            "status": "success",
            "message": f"Selected alternative {selected_index}: {selected_node.thought}",
            "selected_thought": selected_node.thought,
            "current_node_id": selected_node.id
        }
    
    def backtrack(self) -> dict:
        """
        Return to the last high-confidence node in the current path.
        
        Returns:
            Information about backtracking result
        """
        target_node = self.graph.find_last_high_confidence()
        
        if not target_node:
            return {
                "status": "no_target",
                "message": "No high-confidence node found to backtrack to",
                "backtracked_to": None
            }
        
        # Update current node
        self.graph.set_current_node(target_node.id)
        
        return {
            "status": "success",
            "message": f"Backtracked to node {target_node.id}",
            "backtracked_to": {
                "node_id": target_node.id,
                "thought": target_node.thought,
                "confidence": target_node.confidence
            }
        }
    
    def show_current_path(self) -> dict:
        """
        Display the current thinking path.
        
        Returns:
            Current path information
        """
        path_nodes = self.graph.get_path_nodes()
        
        path_info = []
        branch_points = 0
        
        for node in path_nodes:
            path_info.append({
                "node_id": node.id,
                "thought": node.thought,
                "confidence": node.confidence,
                "branch_point": node.branch_point
            })
            if node.branch_point:
                branch_points += 1
        
        return {
            "path": path_info,
            "total_nodes": len(path_info),
            "branch_points": branch_points
        }
    
    def get_unexplored_branches(self) -> dict:
        """
        Find branch points with unexplored alternatives.
        
        Returns:
            Information about unexplored branches
        """
        unexplored = self.graph.get_unexplored_branches()
        
        return {
            "unexplored": unexplored
        }


# Tool definitions for MCP
TOOL_DEFINITIONS = [
    {
        "name": "think",
        "description": "Process a single thought and record it in the graph",
        "inputSchema": {
            "type": "object",
            "properties": {
                "thought": {
                    "type": "string",
                    "description": "The thought content"
                },
                "confidence": {
                    "type": "number",
                    "description": "Confidence level (0.0-1.0)",
                    "minimum": 0.0,
                    "maximum": 1.0
                }
            },
            "required": ["thought", "confidence"]
        }
    },
    {
        "name": "select_path",
        "description": "Choose from alternative thoughts at a branch point",
        "inputSchema": {
            "type": "object",
            "properties": {
                "alternatives": {
                    "type": "array",
                    "description": "List of alternative thoughts",
                    "items": {
                        "type": "object",
                        "properties": {
                            "thought": {
                                "type": "string",
                                "description": "Alternative thought content"
                            },
                            "confidence": {
                                "type": "number",
                                "description": "Confidence level for this alternative",
                                "minimum": 0.0,
                                "maximum": 1.0
                            }
                        },
                        "required": ["thought", "confidence"]
                    }
                },
                "selected_index": {
                    "type": "integer",
                    "description": "Which alternative to select (0-based)",
                    "minimum": 0
                }
            },
            "required": ["alternatives", "selected_index"]
        }
    },
    {
        "name": "backtrack",
        "description": "Return to the last high-confidence node in the current path",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "show_current_path",
        "description": "Display the current thinking path",
        "inputSchema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "get_unexplored_branches",
        "description": "Find branch points with unexplored alternatives",
        "inputSchema": {
            "type": "object",  
            "properties": {}
        }
    }
]
