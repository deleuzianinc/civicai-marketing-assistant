#!/usr/bin/env python3
"""Test script to verify the search module works correctly"""

import os
import sys

# Print diagnostic information
print(f"Current working directory: {os.getcwd()}")
print(f"Script location: {os.path.abspath(__file__)}")
print(f"Script directory: {os.path.dirname(os.path.abspath(__file__))}")

# Try to import and use the search module
try:
    from search_dialogflow_docs import DialogflowDocSearch

    print("\n✓ Successfully imported DialogflowDocSearch")

    # Create searcher instance
    searcher = DialogflowDocSearch()
    print(f"✓ Successfully initialized searcher")
    print(f"  Collection count: {searcher.collection.count()}")

    # Test search
    results = searcher.search("What are playbooks?", n_results=2)
    print(f"\n✓ Search successful!")
    print(f"  Found {len(results['results'])} results")

    if results['results']:
        print(f"\n  First result:")
        print(f"    Section: {results['results'][0]['metadata']['section']}")
        print(f"    Relevance: {results['results'][0]['relevance_score']:.2%}")
        print(f"    Content preview: {results['results'][0]['content'][:100]}...")

except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n✓ All tests passed!")
