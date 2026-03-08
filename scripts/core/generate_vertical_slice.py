#!/usr/bin/env python3
"""
Orchestrator script that dynamically pulls architecture stacks from Memory MCP
and renders complete vertical slices using BlueprintRenderer.
"""

import argparse
import sys
from pathlib import Path

# Note: In a real environment, this would use mcp.clients.memory.MemoryClient
# We simulate the MCP Query logic here.

try:
    from scripts.core.blueprint_renderer import BlueprintRenderer
except ImportError:
    print("Error: Could not import BlueprintRenderer.")
    sys.exit(1)


def query_memory_for_stacks(mcp_node: str) -> list:
    """
    Mock integration of querying the System_Consciousness Memory MCP
    to determine the correct mapping for a logical stack (e.g. 'dotnet_backend').
    """
    print(f"[*] Querying Memory MCP for Node: {mcp_node}...")
    # Simulated result based on Phase 3 output mapping
    registry = {
        "AI_Agent_Layer": "ai/langgraph",
        "Enterprise_Backend": "enterprise/dotnet",
        "Web_Frontend": "web/nextjs",
    }
    return [registry.get(mcp_node, "")]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--slices",
        nargs="+",
        required=True,
        help="List of Memory MCP nodes representing the vertical slice (e.g. AI_Agent_Layer Enterprise_Backend)",
    )
    parser.add_argument(
        "--output", default="./out_vertical_slice", help="Output directory"
    )
    parser.add_argument(
        "--project-name", default="FactoryApp", help="The name of the project"
    )

    args = parser.parse_args()

    # 1. Discover paths via Memory MCP
    resolved_stacks = []
    for node in args.slices:
        paths = query_memory_for_stacks(node)
        valid = [p for p in paths if p]
        if not valid:
            print(
                f"Warning: No valid factory template paths found in Memory for node: {node}"
            )
            continue

        # Build the composition stack node
        resolved_stacks.append({"id": valid[0], "context": {}})

    if not resolved_stacks:
        print("Fatal: No stacks resolved. Cannot proceed.")
        sys.exit(1)

    print(
        f"[*] Memory resolved the following logical paths: {[s['id'] for s in resolved_stacks]}"
    )

    # 2. Build composition payload
    composition = {
        "global_context": {
            "project_name": args.project_name,
            "project_name_pascal": args.project_name.capitalize(),
            "primary_controller_name": "Health",
            "deployment_mode": "cloud",
            "class_prefix": "Agent",
            "node_prefix": "run",
        },
        "stacks": resolved_stacks,
    }

    # 3. Render
    renderer = BlueprintRenderer(target_dir=args.output)
    result = renderer.render_composition(composition)

    if result["success"]:
        print(
            f"\\n[SUCCESS] Vertical Slice successfully generated dynamically in {args.output}"
        )
        for f in result["generated_files"]:
            print(f"  - {f}")
    else:
        print("\\n[ERROR] Generation failed.")
        sys.exit(1)


if __name__ == "__main__":
    main()
