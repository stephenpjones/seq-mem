"""Basic tests for sequential memory functionality."""

import unittest
import sys
import os

# Add parent directory to path to import our modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.sequential_memory.graph import ThoughtGraph, Node, Edge
from src.sequential_memory.tools import SequentialMemoryTools


class TestThoughtGraph(unittest.TestCase):
    """Test the ThoughtGraph class."""
    
    def setUp(self):
        """Set up a fresh graph for each test."""
        self.graph = ThoughtGraph()
    
    def test_node_creation(self):
        """Test creating nodes."""
        node = self.graph.add_node("Test thought", 0.8)
        self.assertEqual(node.id, "node_001")
        self.assertEqual(node.thought, "Test thought")
        self.assertEqual(node.confidence, 0.8)
        self.assertIsNone(node.parent)
        self.assertTrue(node.selected)
        self.assertFalse(node.branch_point)
    
    def test_low_confidence_branch_point(self):
        """Test that low confidence creates branch point."""
        node = self.graph.add_node("Uncertain thought", 0.3)
        self.assertTrue(node.branch_point)
    
    def test_edge_creation(self):
        """Test creating edges between nodes."""
        node1 = self.graph.add_node("First thought", 0.8)
        node2 = self.graph.add_node("Second thought", 0.7, parent=node1.id)
        
        self.assertEqual(len(self.graph.edges), 1)
        edge = self.graph.edges[0]
        self.assertEqual(edge.from_node, node1.id)
        self.assertEqual(edge.to_node, node2.id)
        self.assertTrue(edge.selected)
    
    def test_path_retrieval(self):
        """Test getting path from root to current."""
        node1 = self.graph.add_node("First", 0.8)
        node2 = self.graph.add_node("Second", 0.7, parent=node1.id)
        node3 = self.graph.add_node("Third", 0.9, parent=node2.id)
        
        path = self.graph.get_current_path()
        self.assertEqual(path, ["node_001", "node_002", "node_003"])
    
    def test_backtrack_finding(self):
        """Test finding last high confidence node."""
        node1 = self.graph.add_node("High confidence", 0.8)
        node2 = self.graph.add_node("Low confidence", 0.4, parent=node1.id)
        node3 = self.graph.add_node("Another low", 0.3, parent=node2.id)
        
        target = self.graph.find_last_high_confidence()
        self.assertEqual(target.id, node1.id)
    
    def test_branch_alternatives(self):
        """Test creating branch alternatives."""
        node1 = self.graph.add_node("Branch point", 0.4)
        
        alternatives = [
            {"thought": "Option 1", "confidence": 0.7},
            {"thought": "Option 2", "confidence": 0.6},
            {"thought": "Option 3", "confidence": 0.5}
        ]
        
        selected = self.graph.create_branch_alternatives(alternatives, 1)
        self.assertEqual(selected.thought, "Option 2")
        self.assertTrue(selected.selected)
        
        # Check other alternatives are not selected
        children = self.graph.get_children(node1.id)
        self.assertEqual(len(children), 3)
        selected_count = sum(1 for child in children if child.selected)
        self.assertEqual(selected_count, 1)


class TestSequentialMemoryTools(unittest.TestCase):
    """Test the tools implementation."""
    
    def setUp(self):
        """Set up fresh tools for each test."""
        self.tools = SequentialMemoryTools()
    
    def test_think_high_confidence(self):
        """Test thinking with high confidence."""
        result = self.tools.think("Clear thought", 0.8)
        self.assertEqual(result["status"], "continue")
        self.assertFalse(result["requires_alternatives"])
        self.assertEqual(result["current_node_id"], "node_001")
    
    def test_think_low_confidence(self):
        """Test thinking with low confidence triggers branching."""
        result = self.tools.think("Uncertain thought", 0.3)
        self.assertEqual(result["status"], "branch")
        self.assertTrue(result["requires_alternatives"])
    
    def test_select_path_valid(self):
        """Test selecting a valid path."""
        # First create a branch point
        self.tools.think("Branch point", 0.3)
        
        # Then select from alternatives
        alternatives = [
            {"thought": "Path A", "confidence": 0.7},
            {"thought": "Path B", "confidence": 0.6}
        ]
        result = self.tools.select_path(alternatives, 0)
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["selected_thought"], "Path A")
    
    def test_select_path_invalid_index(self):
        """Test selecting with invalid index."""
        self.tools.think("Branch point", 0.3)
        
        alternatives = [
            {"thought": "Only option", "confidence": 0.7}
        ]
        
        with self.assertRaises(ValueError):
            self.tools.select_path(alternatives, 5)
    
    def test_backtrack_success(self):
        """Test successful backtracking."""
        # Create a path with high and low confidence nodes
        self.tools.think("High confidence start", 0.8)
        self.tools.think("Low confidence middle", 0.4)
        self.tools.think("Another low", 0.3)
        
        result = self.tools.backtrack()
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["backtracked_to"]["node_id"], "node_001")
    
    def test_backtrack_no_target(self):
        """Test backtracking with no high confidence nodes."""
        self.tools.think("Low confidence", 0.3)
        self.tools.think("Another low", 0.4)
        
        result = self.tools.backtrack()
        self.assertEqual(result["status"], "no_target")
    
    def test_show_current_path(self):
        """Test showing the current path."""
        self.tools.think("First", 0.8)
        self.tools.think("Second", 0.3)
        self.tools.think("Third", 0.9)
        
        result = self.tools.show_current_path()
        self.assertEqual(result["total_nodes"], 3)
        self.assertEqual(result["branch_points"], 1)
        self.assertEqual(len(result["path"]), 3)
    
    def test_get_unexplored_branches(self):
        """Test finding unexplored branches."""
        # Create a branch point
        self.tools.think("Branch point", 0.3)
        
        # Create alternatives but only select one
        alternatives = [
            {"thought": "Selected path", "confidence": 0.7},
            {"thought": "Unexplored path", "confidence": 0.6}
        ]
        self.tools.select_path(alternatives, 0)
        
        # Continue on selected path
        self.tools.think("Continue on selected", 0.8)
        
        # Check unexplored branches
        result = self.tools.get_unexplored_branches()
        self.assertEqual(len(result["unexplored"]), 1)
        self.assertEqual(result["unexplored"][0]["unexplored_count"], 1)


class TestEndToEndScenarios(unittest.TestCase):
    """Test complete usage scenarios."""
    
    def setUp(self):
        """Set up fresh tools for each test."""
        self.tools = SequentialMemoryTools()
    
    def test_linear_thinking(self):
        """Test a linear thinking session with no branches."""
        thoughts = [
            ("Understanding the problem", 0.9),
            ("Breaking it down", 0.8),
            ("Finding the solution", 0.7),
            ("Implementing it", 0.8)
        ]
        
        for thought, confidence in thoughts:
            result = self.tools.think(thought, confidence)
            self.assertEqual(result["status"], "continue")
        
        # Check final path
        path = self.tools.show_current_path()
        self.assertEqual(path["total_nodes"], 4)
        self.assertEqual(path["branch_points"], 0)
    
    def test_branch_and_explore(self):
        """Test branching and exploring different paths."""
        # Start with high confidence
        self.tools.think("Starting point", 0.8)
        
        # Hit a branch point
        result = self.tools.think("Uncertain next step", 0.3)
        self.assertEqual(result["status"], "branch")
        
        # Provide alternatives
        alternatives = [
            {"thought": "Approach A", "confidence": 0.7},
            {"thought": "Approach B", "confidence": 0.6},
            {"thought": "Approach C", "confidence": 0.5}
        ]
        
        # Select approach A
        self.tools.select_path(alternatives, 0)
        
        # Continue thinking
        self.tools.think("Developing approach A", 0.8)
        
        # Backtrack to try another approach
        backtrack_result = self.tools.backtrack()
        # Should backtrack to "Approach A" since it has confidence 0.7 (high)
        self.assertEqual(backtrack_result["backtracked_to"]["thought"], "Approach A")
        
        # Check unexplored branches
        unexplored = self.tools.get_unexplored_branches()
        self.assertEqual(len(unexplored["unexplored"]), 1)
        self.assertEqual(unexplored["unexplored"][0]["unexplored_count"], 2)


if __name__ == "__main__":
    unittest.main()
