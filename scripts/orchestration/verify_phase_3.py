import os
import sys


def check_phase_3_gate(design_path):
    """
    Checks if the Phase 3 Gate (Architecture) is satisfied.
    Required Artifact: knowledge/ai-design.md
    """
    if not os.path.exists(design_path):
        print(f"FAILED: Artifact {design_path} not found.")
        return False

    with open(design_path, "r", encoding="utf-8") as f:
        content = f.read()

    required_sections = [
        "# AI System Design",
        "## 1. Architectural Overview",
        "## 2. Component Design",
        "## 3. API Contracts (Draft)",
        "## 4. Architectural Decision Records (ADRs)",
    ]

    missing = []
    for section in required_sections:
        if section not in content:
            missing.append(section)

    if missing:
        print(f"FAILED: {design_path} missing required sections: {', '.join(missing)}")
        return False

    print("SUCCESS: Phase 3 Gate satisfied.")
    return True


if __name__ == "__main__":
    design = "knowledge/ai-design.md"
    if check_phase_3_gate(design):
        sys.exit(0)
    else:
        sys.exit(1)
