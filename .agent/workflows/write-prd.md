---
description: Comprehensive workflow for writing the Product Requirements Document (PRD).
version: 1.0.0
---

# /write-prd Workflow

**Version:** 1.0.0


**Goal:** Transform an approved Prototype Brief into a formal, structured PRD with functional requirements and user stories.

## Steps:
1. **Target**: Load `knowledge/prototype-brief.md`.
2. **Execute**: Trigger `.agent/skills/requirements/writing-prd/SKILL.md`.
3. **Refine**: Trigger `.agent/skills/requirements/slicing-stories/SKILL.md` to ensure stories are vertically sliced.
4. **Template**: Use `knowledge/templates/prd.md`.
5. **Output**: Write to `knowledge/prd.md`.
6. **Follow-up**: Prompt user to run `/elicit-nfr` to complete the technical requirements.


## Trigger Conditions
- Triggered by user context or meta-orchestrator.


## Trigger Examples:
- "Execute this workflow."
