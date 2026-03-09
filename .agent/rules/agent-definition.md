---
trigger: model_decision
---

# Rule: Agent Definition

## Context
Standardizes how agents and personas are defined and specialized in `.agent/agents/`.

## Requirements
- **3-Layer Architecture**:
    1. **Cognitive Layer** (`AGENTS.md`): Defined high-level personas (@Architect, etc.).
    2. **Functional Layer** (`.agent/agents/`): MD definitions for specialized missions.
    3. **Governance Layer** (`.agent/rules/`): Constraints and tactical protocols.
- **Mission First**: Definitions MUST start with a clear Mission Statement and Backstory.
- **Capability Mapping**:
    - Bind specific skills from `.agent/skills/`.
    - Define tool access and limitations.
- **Axiom Continuity**:
    - Agent behavior MUST align with `.agentrules`.
- **Contextual Consciousness**:
    - Agents MUST be designed with a "MCP-First" grounding mindset.
    - Definitions MUST specify which MCP servers the agent is authorized to manage.

## Process
1. Identify missing specialization.
2. Design persona and backstory (Phase 1 of `agent-development` workflow).
3. Draft agent definition file in `.agent/agents/`.
4. Bind required skills and knowledge.
5. Register in `agent-staffing.json` including the correct `@persona` mapping.
