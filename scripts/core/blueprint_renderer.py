#!/usr/bin/env python3
"""
Antigravity Agent Factory - Multi-Stack Blueprint Renderer

This module provides the core engine for scaffolding functional code templates
across multiple technology stacks (AI, Enterprise, Web) into a target repository.

Usage:
    from scripts.core.blueprint_renderer import BlueprintRenderer

    renderer = BlueprintRenderer(target_dir="out/my_project")
    renderer.render_stack("ai/langgraph", context={"project_name": "demo"})

"""

import json
import os
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    from scripts.core.template_engine import TemplateEngine, create_engine
except ImportError:
    print("Error: Could not import TemplateEngine from scripts.core.template_engine")
    import sys

    sys.exit(1)


class BlueprintRenderer:
    """
    Renders multi-stack code templates into a target directory.
    """

    def __init__(self, target_dir: str, factory_root: Optional[Path] = None):
        """
        Initialize the blueprint renderer.

        Args:
            target_dir: The destination directory for the generated code.
            factory_root: Root directory of the factory containing the templates.
        """
        self.target_dir = Path(target_dir)
        self.factory_root = factory_root or Path(__file__).parent.parent.parent
        self.templates_dir = self.factory_root / "src" / "templates"

        # We include src/templates as an additional dir for the engine so Jinja
        # can correctly resolve complex include/extend paths for code generation.
        self.engine = create_engine(
            factory_root=self.factory_root, additional_dirs=[self.templates_dir]
        )

        self.generated_files: List[str] = []
        self.errors: List[str] = []

    def load_composition(self, composition_file: str) -> Dict[str, Any]:
        """
        Load a JSON composition file detailing the stacks and contexts to render.
        """
        path = Path(composition_file)
        if not path.exists():
            raise FileNotFoundError(f"Composition file not found: {path}")

        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def render_stack(self, stack_path: str, context: Dict[str, Any]) -> bool:
        """
        Render a specific template stack directory into the target.

        Args:
            stack_path: Relative path inside `src/templates/` (e.g. 'ai/langgraph')
            context: Jinja context variables injected into the templates.
        """
        source_dir = self.templates_dir / stack_path

        if not source_dir.exists() or not source_dir.is_dir():
            err = f"Stack template directory not found: {source_dir}"
            self.errors.append(err)
            print(f"Error: {err}")
            return False

        print(f"Rendering stack '{stack_path}' into {self.target_dir}")

        success = True
        for root, _, files in os.walk(source_dir):
            root_path = Path(root)
            rel_root = root_path.relative_to(source_dir)

            for file_name in files:
                src_file = root_path / file_name

                # Strip .j2 or .tmpl from the output filename
                dest_file_name = file_name
                is_template = False
                if file_name.endswith((".j2", ".tmpl")):
                    dest_file_name = file_name.rsplit(".", 1)[0]
                    is_template = True

                # Process destination path with Jinja context to allow dynamic folder names
                try:
                    rel_dest_dir_str = self.engine.render_string(str(rel_root), context)
                    dest_file_name_str = self.engine.render_string(
                        dest_file_name, context
                    )
                except Exception as e:
                    err = f"Failed to render path '{rel_root}/{dest_file_name}': {e}"
                    self.errors.append(err)
                    print(f"Warning: {err}")
                    success = False
                    continue

                dest_dir = self.target_dir / rel_dest_dir_str
                dest_dir.mkdir(parents=True, exist_ok=True)
                dest_file = dest_dir / dest_file_name_str

                try:
                    if is_template:
                        # Process file contents using the template engine
                        content = self.engine.render_file(src_file, context)
                        with open(dest_file, "w", encoding="utf-8") as f:
                            f.write(content)
                    else:
                        # Straight copy for binary files or non-templates
                        shutil.copy2(src_file, dest_file)

                    self.generated_files.append(str(dest_file))
                except Exception as e:
                    err = f"Failed to render file '{src_file}': {e}"
                    self.errors.append(err)
                    print(f"Error: {err}")
                    success = False

        return success

    def render_composition(self, composition: Dict[str, Any]) -> Dict[str, Any]:
        """
        Renders a full composition object comprising multiple stacks.
        """
        self.target_dir.mkdir(parents=True, exist_ok=True)

        stacks = composition.get("stacks", [])
        global_context = composition.get("global_context", {})

        for stack in stacks:
            stack_id = stack.get("id")
            if not stack_id:
                continue

            # Merge global context with stack-specific context
            merged_context = {**global_context, **stack.get("context", {})}
            # Add some automatic context metadata
            merged_context["__stack_id__"] = stack_id

            self.render_stack(stack_id, merged_context)

        return {
            "success": len(self.errors) == 0,
            "target_dir": str(self.target_dir),
            "generated_files": self.generated_files,
            "errors": self.errors,
        }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Multi-Stack Blueprint Renderer")
    parser.add_argument(
        "--composition", "-c", required=True, help="Path to composition JSON file"
    )
    parser.add_argument(
        "--output", "-o", default="./out", help="Target output directory"
    )

    args = parser.parse_args()

    renderer = BlueprintRenderer(target_dir=args.output)
    try:
        comp_data = renderer.load_composition(args.composition)
        result = renderer.render_composition(comp_data)

        if result["success"]:
            print(
                f"\\nSUCCESS: Scaffolded {len(result['generated_files'])} files into {result['target_dir']}"
            )
        else:
            print(f"\\nWARNING: Completed with {len(result['errors'])} errors.")
    except Exception as e:
        print(f"FATAL: {e}")
        import sys

        sys.exit(1)
