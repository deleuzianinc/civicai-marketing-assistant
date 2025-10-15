from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import asyncio
import sys

app = Server("dialogflow-documentation")

# Don't initialize these at startup - lazy load them
searcher = None

def get_searcher():
    """Lazy load the search functionality"""
    global searcher
    if searcher is None:
        try:
            import os
            from search_dialogflow_docs import DialogflowDocSearch

            # Debug: Print working directory and paths
            script_dir = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(script_dir, "dialogflow_chroma_db")
            print(f"MCP Server script dir: {script_dir}", file=sys.stderr)
            print(f"Expected DB path: {db_path}", file=sys.stderr)
            print(f"DB exists: {os.path.exists(db_path)}", file=sys.stderr)

            searcher = DialogflowDocSearch()
            print("Search engine initialized", file=sys.stderr)
        except Exception as e:
            print(f"Failed to initialize searcher: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc(file=sys.stderr)
            raise
    return searcher

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="search_dialogflow_docs",
            description="Search the Dialogflow CX documentation for information about APIs, concepts, and how-to guides",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query or question"
                    },
                    "n_results": {
                        "type": "integer",
                        "description": "Number of results to return (default: 5)",
                        "default": 5
                    }
                },
                "required": ["query"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "search_dialogflow_docs":
        try:
            # Lazy load searcher only when tool is called
            search_engine = get_searcher()
            
            query = arguments["query"]
            n_results = arguments.get("n_results", 5)
            
            results = search_engine.search(query, n_results)
            
            if not results['results']:
                return [TextContent(
                    type="text",
                    text="No relevant information found in the documentation."
                )]
            
            # Format results
            formatted = []
            for i, result in enumerate(results['results'], 1):
                formatted.append(f"**Result {i}** (Relevance: {result['relevance_score']:.0%})")
                formatted.append(f"Section: {result['metadata']['section']}")
                formatted.append(f"\n{result['content']}\n")
                formatted.append("---")
            
            return [TextContent(
                type="text",
                text="\n".join(formatted)
            )]
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"Error searching documentation: {str(e)}"
            )]
    
    return [TextContent(type="text", text=f"Unknown tool: {name}")]

async def main():
    print("MCP server starting...", file=sys.stderr)
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
