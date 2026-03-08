# Antigravity Agent Factory: SDLC Concept Paper (V2)

## 1. Executive Summary
The Antigravity SDLC (Agentic Software Development Life Cycle) is a high-fidelity, orchestrator-led framework for building software with AI agents. It moves beyond "chat-and-code" to a systematic, phased approach where every artifact is grounded in requirements and verified by adversarial agents. This document defines the backbone of the factory's operational model.

## 2. The 7-Phase Orchestration Framework

### 2.1 Workflow & Skill Matrix
| Phase | Goal | Agent Role | Key Workflows | Primary Skills | Gate Artifact |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **P1: Ideation** | Define Vision | `workflow-architect` | `/brainstorm`, `/cluster` | `framing-problems`, `brainstorming-ideas`, `scanning-competition` | `prototype-brief.md` |
| **P2: Requirements** | Define "Ready" | `workflow-architect` | `/write-prd`, `/elicit-nfr` | `writing-prd`, `eliciting-nfr`, `slicing-stories`, `reviewing-requirements` | `prd.md` |
| **P3: Architecture** | Define System | `workflow-architect` | `/ai-system-design` | `designing-ai-systems`, `designing-apis`, `mapping-dependencies` | `ai-design.md`, ADRs |
| **P4: Build** | Implementation | `template-generator` | `/agent-development` | `generating-templates`, `developing-fastapi`, `developing-nextjs` | Codebase / PR |
| **P5: Test & Eval** | Verification | `test-conductor` | `/agent-testing`, `/eda` | `reviewing-clean-code`, `testing-frontend`, `verifying-artifact-structures` | `eval-report.md` |
| **P6: Deploy** | Release | `registry-clerk` | `/committing-releases` | `committing-releases`, `containerizing-java-apps` | `CHANGELOG.md` |
| **P7: Monitor** | Observation | `integrity-guardian` | `/debug-pipeline` | `monitoring-ml-models`, `tracing-with-langsmith`, `optimizing-prompts` | `telemetry.md` |

---

## 3. Orchestration Logic

### 3.1 Intra-Phase Orchestration (The Loop)
Within a single phase, the `primary_agent` executes a specialized "Agentic Loop":
1.  **Draft**: Generate a draft using phase-specific skills.
2.  **Critique**: Trigger an adversarial review (e.g., `reviewing-requirements`).
3.  **Refine**: Iterate based on critique.
4.  **Handoff**: Prepare the Gate Artifact for human sign-off.

### 3.2 Meta-Orchestration (The Spine)
The **SDLC Meta-Orchestrator** (workflow) manages long-running state:
- **State Management**: Persists the current phase in `.agent/knowledge/sdlc-architecture-graph.json`.
- **Gatekeeping**: Blocks progress to Phase N+1 until the Gate Artifact for Phase N is "Approved".
- **Asset Pointers**: Updates the Knowledge Graph with pointers to the latest PRDs, Designs, and Test Reports.

---

## 4. Plane PMS Integration Architecture

To ensure high-fidelity tracking, the factory mirrors its internal state in Plane using the following hierarchy:

| Object | Plane Component | Logic |
| :--- | :--- | :--- |
| **Major Goal** | **Parent Issue** | The high-level objective (e.g., "Build Auth System"). |
| **SDLC Phases** | **Child Issues** | Each of the 7 phases is a child task linked to the parent. |
| **Categorization** | **Modules** | Use Modules named `01-Ideation`, `02-Requirements`, etc., for cross-project phase analysis. |
| **Time Boxing** | **Cycles** | Group phase execution into measurable sprints. |
| **Technical Spec** | **Description HTML** | Every ticket MUST follow the `task_definition_schema.json` within its description. |

---

## 5. Factory Realization Path

### 5.1 Knowledge Layer
- **Memory Graph**: `sdlc-architecture-graph.json` maps relationships (e.g., "PRD-1 requires Brief-1").
- **Asset Registry**: `agent-team-registry.json` ensures roles match capabilities.

### 5.2 Command Layer
- **Slash Commands**: Unified workflows in `.agent/workflows/` act as the entry points for each phase.
- **Always-on Rules**: `.agent/rules/` (e.g., `plane-task-governance.md`) enforce the schema during every interaction.

### 5.3 Infrastructure Layer (MCP)
- **Memory MCP**: The bridge for the Knowledge Graph.
- **Plane MCP**: Remote sync of issue state and metadata.
- **Search MCP**: Competitive and technical grounding.

---

## 6. Realization Strategy (Phased implementation)
1.  **Grounding**: Establish the central documentation and schemas (Complete).
2.  **Tooling Upgrade**: Patch templates (`work_item.html.j2`) and skills to support the schema.
3.  **Pilot Execution**: Run a full 7-phase cycle for a new internal "Self-Correction" skill.
4.  **Feedback Loop**: P7 (Monitor) updates the SDLC rules themselves based on agent performance.
