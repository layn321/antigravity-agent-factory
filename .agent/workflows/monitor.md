---
description: Comprehensive workflow for production monitoring and feedback loops.
version: 1.0.0
---

# /monitor Workflow

**Version:** 1.0.0


**Goal:** Track feature health in production, harvest user feedback, and feed insights back into the Ideation phase for continuous improvement.

## Steps:
1. **Target**: Load `knowledge/release-notes.md`.
2. **Execute**: Trigger `.agent/skills/logging-and-monitoring/SKILL.md`.
3. **Audit**: Trigger `.agent/skills/releases/governing-repositories/SKILL.md` (audit section).
4. **Report**: Generate `monitor-report.md` using `knowledge/templates/monitor-report.md`.
5. **Output**: Write findings to `knowledge/monitor-report.md`.
6. **Cycle Completion**: Propose the final "Closure" of the Plane issue and feed new ideas back to `/brainstorm`.

## Phase Gate (Monitor):
- Mandatory generation of `monitor-report.md`.
- Feedback loop closed.


## Trigger Conditions
- Triggered by user context or meta-orchestrator.


## Trigger Examples:
- "Execute this workflow."
