"""Main MCP server implementation for sequential memory."""

import json
import logging
import sys
from typing import Any, Dict

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from .tools import SequentialMemoryTools, TOOL_DEFINITIONS


# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger(__name__)


class SequentialMemoryServer:
    """MCP server for sequential thinking with memory."""
    
    def __init__(self):
        """Initialize the server and tools."""
        self.tools = SequentialMemoryTools()
        self.server = Server("sequential-memory")
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Set up the MCP protocol handlers."""
        
        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            """Return the list of available tools."""
            return [
                Tool(**tool_def) for tool_def in TOOL_DEFINITIONS
            ]
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]) -> list[TextContent]:
            """Handle tool calls."""
            try:
                # Route to appropriate tool handler
                if name == "think":
                    result = self.tools.think(
                        thought=arguments["thought"],
                        confidence=arguments["confidence"]
                    )
                elif name == "select_path":
                    result = self.tools.select_path(
                        alternatives=arguments["alternatives"],
                        selected_index=arguments["selected_index"]
                    )
                elif name == "backtrack":
                    result = self.tools.backtrack()
                elif name == "show_current_path":
                    result = self.tools.show_current_path()
                elif name == "get_unexplored_branches":
                    result = self.tools.get_unexplored_branches()
                else:
                    result = {"error": f"Unknown tool: {name}"}
                
                # Return result as JSON text
                return [TextContent(
                    type="text",
                    text=json.dumps(result, indent=2)
                )]
                
            except Exception as e:
                logger.error(f"Error in tool {name}: {str(e)}")
                error_result = {
                    "error": str(e),
                    "tool": name
                }
                return [TextContent(
                    type="text",
                    text=json.dumps(error_result, indent=2)
                )]
    
    async def run(self):
        """Run the server."""
        async with stdio_server() as (read_stream, write_stream):
            logger.info("Sequential Memory MCP Server starting...")
            await self.server.run(read_stream, write_stream)


def main():
    """Main entry point."""
    import asyncio
    
    server = SequentialMemoryServer()
    try:
        asyncio.run(server.run())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
