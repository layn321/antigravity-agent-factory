---
description: Formalizes a selected opportunity into a Prototype Brief (Phase 1 Gate).
version: 1.0.0
---

# /brief-prototype Workflow

**Version:** 1.0.0


**Goal:** Transform a prioritized opportunity cluster into a formal, human-approvable Prototype Brief.

## Steps:
1. **Target**: Load `knowledge/opportunities.md`.
2. **Execute**: Trigger `.agent/skills/ideation/briefing-prototypes/SKILL.md`.
3. **Template**: Use `knowledge/templates/prototype-brief.md`.
4. **Output**: Write to `knowledge/prototype-brief.md`.
5. **Phase Gate**: Ask the user for explicit approval and sign-off on the brief before moving to Phase 2 (Requirements).


## Trigger Conditions
- Triggered by user context or meta-orchestrator.


## Trigger Examples:
- "Execute this workflow."
