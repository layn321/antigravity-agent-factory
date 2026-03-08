---
description: Workflow for designing, building, and structuring the antigravity-factory system itself using SDLC phases.
agents:
  - workflow-architect
  - template-generator
version: 1.0.0
---

# Antigravity Factory System Building Process

**Version:** 1.0.0


This is the meta-workflow for building out the antigravity-agent-factory. It strictly follows the 7-Phase AI SDLC Process to convert abstract ideas into formal systemic capabilities.

## Phases
This factory utilizes a 7-phase flow. Each phase requires a human-approved phase gate artifact before advancing.

### 1. Ideation
- **Input**: Raw idea or pain point
- **Skills**: `framing-problems`, `brainstorming-ideas`
- **Output**: `knowledge/prototype-brief.md` (Must be human-approved)

### 2. Requirements
- **Input**: Approved `prototype-brief.md`
- **Output**: Formal `knowledge/prd.md` and Plane Issues.
- **Action**: Trigger `plane-task-management.md` workflow to formalize epics and issues in Plane PMS.

### 3. Architecture
- **Input**: Approved PRD
- **Output**: Implementation Plan, ADRs, System Design specs.
- **Action**: Update Memory Graph (Memory MCP) with new architectural nodes and relationships.

### 4. Build
- **Input**: Architecture Docs
- **Action**: TDD implementation. Create the actual workflows (`.agent/workflows/`), skills (`.agent/skills/`), and knowledge documents (`.agent/knowledge/`).
- **Output**: Working Implementation.

### 5. Test & Eval
- **Input**: Working Implementation
- **Action**: Run `pytest`, `tox`, or equivalent automated test suites to validate systemic integrity.

### 6. Deploy
- **Input**: Tested Implementation
- **Action**: Formal git commit via `committing-releases` skill.
- **Output**: Tagged release.

### 7. Monitor & Closure
- **Input**: Live system
- **Action**: Sync the completed architectural insights to Plane using `post_solution.py` in the `managing-plane-tasks` skill.

## Systematic Structuring & Hierarchical Cataloging
When adding new workflows, agents, or skills:
1. Define the component's strict inputs and outputs.
2. Register the component within the appropriate SDLC phase folder or tagging structure.
3. Update the overarching Knowledge Graph via MCP Memory to establish semantic ties (e.g. `Workflow X uses Agent Y uses Skill Z`).


## Trigger Conditions
- Triggered by user context or meta-orchestrator.


## Trigger Examples:
- "Execute this workflow."
