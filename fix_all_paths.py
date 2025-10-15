#!/usr/bin/env python3
"""
Fix ALL resource paths in the export to use Git Export format.

This removes ALL full resource paths and converts them to:
- UUIDs for name fields
- displayNames for references
"""

import json
import pathlib
import uuid

def generate_uuid():
    """Generate a UUID."""
    return str(uuid.uuid4())

def fix_page_file(file_path: pathlib.Path):
    """Fix a page JSON file."""
    print(f"Fixing page: {file_path}")
    data = json.loads(file_path.read_text(encoding="utf-8"))

    # Fix name field - replace full path with UUID
    if "name" in data and isinstance(data["name"], str) and "projects/" in data["name"]:
        data["name"] = generate_uuid()
        print(f"  Fixed name to UUID")

    # Fix form parameters - entity types
    if "form" in data and "parameters" in data["form"]:
        for param in data["form"]["parameters"]:
            if "entityType" in param and isinstance(param["entityType"], str) and "projects/" in param["entityType"]:
                # Extract just the entity type name
                parts = param["entityType"].split("/")
                if "sys." in param["entityType"]:
                    # System entity - keep as is
                    pass
                else:
                    # Custom entity - use just the last part
                    entity_name = parts[-1] if parts else param["entityType"]
                    param["entityType"] = entity_name
                    print(f"  Fixed entityType reference")

    # Fix entry fulfillment webhooks
    if "entryFulfillment" in data and "webhook" in data["entryFulfillment"]:
        webhook = data["entryFulfillment"]["webhook"]
        if isinstance(webhook, str) and "projects/" in webhook:
            # Extract displayName from path
            parts = webhook.split("/")
            webhook_name = parts[-1] if parts else webhook
            data["entryFulfillment"]["webhook"] = webhook_name
            print(f"  Fixed webhook reference")

    # Fix transition routes
    if "transitionRoutes" in data:
        for route in data["transitionRoutes"]:
            # Fix intent references
            if "intent" in route and isinstance(route["intent"], str) and "projects/" in route["intent"]:
                parts = route["intent"].split("/")
                intent_name = parts[-1] if parts else route["intent"]
                route["intent"] = intent_name
                print(f"  Fixed intent reference")

            # Fix target page references
            if "targetPage" in route and isinstance(route["targetPage"], str) and "projects/" in route["targetPage"]:
                parts = route["targetPage"].split("/")
                page_name = parts[-1] if parts else route["targetPage"]
                route["targetPage"] = page_name
                print(f"  Fixed targetPage reference")

            # Fix target flow references
            if "targetFlow" in route and isinstance(route["targetFlow"], str) and "projects/" in route["targetFlow"]:
                parts = route["targetFlow"].split("/")
                # Check if it's default-start-flow
                if "default-start-flow" in route["targetFlow"]:
                    route["targetFlow"] = "00000000-0000-0000-0000-000000000000"
                else:
                    flow_name = parts[-1] if parts else route["targetFlow"]
                    route["targetFlow"] = flow_name
                print(f"  Fixed targetFlow reference")

            # Fix fulfillment webhooks
            if "triggerFulfillment" in route and "webhook" in route["triggerFulfillment"]:
                webhook = route["triggerFulfillment"]["webhook"]
                if isinstance(webhook, str) and "projects/" in webhook:
                    parts = webhook.split("/")
                    webhook_name = parts[-1] if parts else webhook
                    route["triggerFulfillment"]["webhook"] = webhook_name
                    print(f"  Fixed route webhook reference")

    # Write back
    file_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def fix_agent_json(file_path: pathlib.Path):
    """Fix agent.json to remove project-specific names."""
    print(f"Fixing agent.json: {file_path}")
    data = json.loads(file_path.read_text(encoding="utf-8"))

    # Remove the name field entirely - it will be set by the target project
    if "name" in data:
        del data["name"]
        print(f"  Removed name field (will be set by target project)")

    # Write back
    file_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def main():
    """Fix all resource paths in the export."""
    src_dir = pathlib.Path(__file__).parent / "src"

    print("Fixing all resource paths to Git Export format...\n")

    # Fix agent.json
    print("=== Fixing agent.json ===")
    agent_json = src_dir / "agent.json"
    if agent_json.exists():
        fix_agent_json(agent_json)
    print()

    # Fix all page files
    print("=== Fixing Page Files ===")
    for page_file in src_dir.glob("flows/*/pages/*.json"):
        fix_page_file(page_file)
    # Also check subdirectory pages
    for page_file in src_dir.glob("flows/*/*/*.json"):
        if page_file.parent.name not in ["pages", "transitionRouteGroups"]:
            fix_page_file(page_file)
    print()

    print("✓ All paths fixed!")
    print("\nNext step: Create ZIP and import to Dialogflow CX")

if __name__ == "__main__":
    main()
