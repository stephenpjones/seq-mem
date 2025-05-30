"""In-memory graph implementation for sequential thinking with memory."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import json


@dataclass
class Node:
    """Represents a thought node in the graph."""
    id: str
    thought: str
    confidence: float
    parent: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    selected: bool = True
    branch_point: bool = False
    
    def to_dict(self) -> dict:
        """Convert node to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "thought": self.thought,
            "confidence": self.confidence,
            "parent": self.parent,
            "created_at": self.created_at,
            "selected": self.selected,
            "branch_point": self.branch_point
        }


@dataclass
class Edge:
    """Represents a connection between thoughts."""
    from_node: str
    to_node: str
    selected: bool = True
    
    def to_dict(self) -> dict:
        """Convert edge to dictionary for JSON serialization."""
        return {
            "from": self.from_node,
            "to": self.to_node,
            "selected": self.selected
        }


class ThoughtGraph:
    """Manages the thought graph structure and operations."""
    
    def __init__(self):
        """Initialize an empty thought graph."""
        self.nodes: Dict[str, Node] = {}
        self.edges: List[Edge] = []
        self.current_node: Optional[str] = None
        self.node_counter: int = 0
    
    def _generate_node_id(self) -> str:
        """Generate a unique node ID."""
        self.node_counter += 1
        return f"node_{self.node_counter:03d}"
    
    def add_node(self, thought: str, confidence: float, 
                 parent: Optional[str] = None, selected: bool = True) -> Node:
        """Add a new thought node to the graph."""
        node_id = self._generate_node_id()
        node = Node(
            id=node_id,
            thought=thought,
            confidence=confidence,
            parent=parent,
            selected=selected,
            branch_point=(confidence < 0.6)
        )
        self.nodes[node_id] = node
        
        # Add edge from parent if exists
        if parent and parent in self.nodes:
            edge = Edge(from_node=parent, to_node=node_id, selected=selected)
            self.edges.append(edge)
        
        # Update current node if this is selected
        if selected:
            self.current_node = node_id
        
        return node
    
    def get_current_path(self) -> List[str]:
        """Get the path from root to current node."""
        if not self.current_node:
            return []
        
        path = []
        node_id = self.current_node
        
        while node_id:
            path.append(node_id)
            node = self.nodes.get(node_id)
            if node:
                node_id = node.parent
            else:
                break
        
        return list(reversed(path))
    
    def get_path_nodes(self) -> List[Node]:
        """Get all nodes in the current path."""
        path_ids = self.get_current_path()
        return [self.nodes[node_id] for node_id in path_ids if node_id in self.nodes]
    
    def find_last_high_confidence(self) -> Optional[Node]:
        """Find the last high-confidence node in the current path."""
        path_nodes = self.get_path_nodes()
        
        # Traverse backwards to find high confidence node
        for node in reversed(path_nodes[:-1]):  # Exclude current node
            if node.confidence >= 0.6:
                return node
        
        return None
    
    def set_current_node(self, node_id: str) -> bool:
        """Set the current node pointer."""
        if node_id in self.nodes:
            self.current_node = node_id
            return True
        return False
    
    def get_children(self, node_id: str) -> List[Node]:
        """Get all child nodes of a given node."""
        children = []
        for edge in self.edges:
            if edge.from_node == node_id and edge.to_node in self.nodes:
                children.append(self.nodes[edge.to_node])
        return children
    
    def get_unexplored_branches(self) -> List[dict]:
        """Find all branch points with unexplored alternatives."""
        unexplored = []
        
        for node_id, node in self.nodes.items():
            if node.branch_point:
                children = self.get_children(node_id)
                unselected = [child for child in children if not child.selected]
                
                if unselected:
                    unexplored.append({
                        "branch_node_id": node_id,
                        "branch_thought": node.thought,
                        "unexplored_count": len(unselected),
                        "alternatives": [
                            {
                                "node_id": child.id,
                                "thought": child.thought,
                                "confidence": child.confidence
                            }
                            for child in unselected
                        ]
                    })
        
        return unexplored
    
    def mark_edges_to_node(self, node_id: str, selected: bool):
        """Mark all edges leading to a node as selected/unselected."""
        for edge in self.edges:
            if edge.to_node == node_id:
                edge.selected = selected
    
    def create_branch_alternatives(self, alternatives: List[dict], 
                                 selected_index: int) -> Optional[Node]:
        """Create alternative nodes at a branch point."""
        if not self.current_node:
            return None
        
        parent_id = self.current_node
        created_nodes = []
        
        # Create all alternative nodes
        for i, alt in enumerate(alternatives):
            is_selected = (i == selected_index)
            node = self.add_node(
                thought=alt["thought"],
                confidence=alt["confidence"],
                parent=parent_id,
                selected=is_selected
            )
            created_nodes.append(node)
        
        # Return the selected node
        if 0 <= selected_index < len(created_nodes):
            return created_nodes[selected_index]
        
        return None
    
    def to_dict(self) -> dict:
        """Convert the entire graph to a dictionary."""
        return {
            "nodes": {node_id: node.to_dict() for node_id, node in self.nodes.items()},
            "edges": [edge.to_dict() for edge in self.edges],
            "current_node": self.current_node,
            "node_counter": self.node_counter
        }
