import json
import os
import shutil
from pathlib import Path

import pytest
from scripts.core.blueprint_renderer import BlueprintRenderer


@pytest.fixture
def temp_workspace(tmp_path):
    """
    Creates a temporary workspace containing mock templates and an output dir.
    """
    factory_dir = tmp_path / "factory"
    templates_dir = factory_dir / "src" / "templates"
    templates_dir.mkdir(parents=True)

    # Mock an AI LangGraph stack
    lg_dir = templates_dir / "ai" / "langgraph"
    lg_dir.mkdir(parents=True)

    # Create a template file: node.py.j2
    (lg_dir / "node.py.j2").write_text(
        "def {{ function_name }}():\\n    print('Hello {{ project_name }}!')"
    )

    # Create a raw file: graph.json
    (lg_dir / "graph.json").write_text('{"nodes": ["{{ function_name }}"]}')

    # Output directory
    out_dir = tmp_path / "out"
    out_dir.mkdir()

    return {"factory_root": factory_dir, "out_dir": out_dir, "templates": templates_dir}


def test_renderer_initialization(temp_workspace):
    renderer = BlueprintRenderer(
        target_dir=str(temp_workspace["out_dir"]),
        factory_root=temp_workspace["factory_root"],
    )
    assert renderer.templates_dir.exists()


def test_render_stack_success(temp_workspace):
    renderer = BlueprintRenderer(
        target_dir=str(temp_workspace["out_dir"]),
        factory_root=temp_workspace["factory_root"],
    )

    context = {"function_name": "run_agent", "project_name": "TestAI"}
    success = renderer.render_stack("ai/langgraph", context)

    assert success is True
    assert len(renderer.generated_files) == 2

    # Verify rendered template
    node_file = temp_workspace["out_dir"] / "node.py"
    assert node_file.exists()
    content = node_file.read_text()
    assert "def run_agent():" in content
    assert "print('Hello TestAI!')" in content

    # Verify straight copy (non .j2)
    graph_file = temp_workspace["out_dir"] / "graph.json"
    assert graph_file.exists()
    # Ensure it didn't get templated because it lacks .j2
    graph_content = graph_file.read_text()
    assert '{"nodes": ["{{ function_name }}"]}' in graph_content


def test_render_composition(temp_workspace):
    # Setup test composition
    comp_file = temp_workspace["factory_root"] / "comp.json"
    comp_data = {
        "global_context": {"project_name": "GlobalTest"},
        "stacks": [{"id": "ai/langgraph", "context": {"function_name": "agent_x"}}],
    }
    comp_file.write_text(json.dumps(comp_data))

    renderer = BlueprintRenderer(
        target_dir=str(temp_workspace["out_dir"]),
        factory_root=temp_workspace["factory_root"],
    )

    loaded_data = renderer.load_composition(str(comp_file))
    result = renderer.render_composition(loaded_data)

    assert result["success"] is True
    node_file = temp_workspace["out_dir"] / "node.py"
    assert "agent_x" in node_file.read_text()
    assert "GlobalTest" in node_file.read_text()
