#!/usr/bin/env python3
"""Test if MCP server can import and use search module"""

import os
import sys

print(f"Python path: {sys.path[:3]}")
print(f"Current working directory: {os.getcwd()}")

# Simulate what the MCP server does
try:
    # Import exactly as the MCP server does
    from search_dialogflow_docs import DialogflowDocSearch

    print("\n✓ Import successful")

    # Initialize exactly as the MCP server does
    searcher = DialogflowDocSearch()

    print(f"✓ Initialization successful")
    print(f"  Collection: {searcher.collection.name}")
    print(f"  Count: {searcher.collection.count()}")

    # Test search
    results = searcher.search("webhooks", n_results=1)
    print(f"\n✓ Search successful: {len(results['results'])} results")

except Exception as e:
    print(f"\n✗ Failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
