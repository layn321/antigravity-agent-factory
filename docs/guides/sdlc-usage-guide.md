# Antigravity SDLC Usage Guide

This guide describes the 7 phases of the Automated Software Development Life Cycle (SDLC) used in the Antigravity Agent Factory. Every phase is enforced by a specific workflow and requires a formal "Phase Gate" artifact before proceeding.

---

## The Axiomatic Foundation
The SDLC is grounded in the **5-Layer Deductive-Inductive Architecture**. Every line of code or documentation produced is checked against **Axiom 0 (Love, Truth, Beauty)** via the **Integrity Guardian**.

> **"No Code without a Gate. No Release without a Note."**

---

## SDLC Phase Overview

| Phase | Goal | Primary Workflow | Gate Artifact |
| :--- | :--- | :--- | :--- |
| **P1: Ideation** | Transform vague requests into formal, approvable briefs. | `/brief-prototype` | `knowledge/prototype-brief.md` |
| **P2: Requirements** | Transform briefs into structured PRDs and NFRs. | `/write-prd` | `knowledge/prd.md` |
| **P3: Architecture** | Design robust, scalable, and cost-effective systems. | `/ai-system-design` | `knowledge/ai-design.md` |
| **P4: Build** | Safe, axiomatic implementation with automated walkthroughs. | `/feature-development` | `knowledge/walkthrough.md` |
| **P5: Test & Eval** | Verification against requirements via rigorous evaluation. | `/agent-testing` | `knowledge/eval-report.md` |
| **P6: Deploy** | Coordinate deployment, versioning, and formal release. | `/release-management` | `knowledge/release-notes.md` |
| **P7: Monitor** | Track production health and feed insights back to P1. | `/monitor` | `knowledge/monitor-report.md` |

---

## Workflow Interaction Patterns

Working with the Antigravity system involves a specific "Call-and-Response" pattern. Each workflow is designed to be highly interactive, guiding you through the axiomatic verification steps.

### IDE Interaction (Slash Commands)
- **Direct Trigger**: Type `@[/workflow-name]` in the developer prompt.
- **Context Awareness**: The agent reads your open files and cursor position to "prime" the workflow.
- **Verification Gates**: Agents will often pause and ask for your approval using the `notify_user` system before making destructive changes.

### CLI Interaction (Automated)
Many workflows can be triggered or inspected via the CLI for CI/CD or batch operations:
```powershell
# List all available workflows
conda run -p D:\Anaconda\envs\cursor-factory python cli/factory_cli.py list-workflows

# Execute a specific workflow
conda run -p D:\Anaconda\envs\cursor-factory python cli/factory_cli.py run-workflow feature-development --project AGENT-123
```

---

## Phase Deep Dives & Workflow Triggers

### P1: Ideation (The Spark)
*   **Why it Matters**: Prevents wasted effort on poorly defined or low-ROI features.
*   **Real-World Example**: A user asks for "better memory." P1 brainstorms alternatives (Long-term RAG vs. Episodic Memory) and converges on a memory persistence brief.
*   **Workflow**: `@[/brainstorm]`, `@[/cluster]`, `@[/brief-prototype]`
*   **How to Work with it**: Start with `/brainstorm` to generate high-volume ideas. Then use `/cluster` to group them into "Opportunity Clusters." Finally, `/brief-prototype` formalizes one cluster into a persistent artifact.
*   **Gate Artifact**: `knowledge/prototype-brief.md`

### P2: Requirements (The Blueprint)
*   **Why it Matters**: Establishes the "Truth" against which the system is verified.
*   **Real-World Example**: Defining the exact fields for a User Profile and the latency requirements (NFRs) for retrieval.
*   **Workflow**: `@[/write-prd]`, `@[/elicit-nfr]`, `@[/review-requirements]`
*   **How to Work with it**: Provide the Prototype Brief as context. The agent will draft a PRD. Use `/elicit-nfr` to "Socratically" discover non-functional constraints through a Q&A session.
*   **Gate Artifact**: `knowledge/prd.md`

### P3: Architecture (The Skeleton)
*   **Why it Matters**: Ensures the system is "Beautiful" structurally and technically sound.
*   **Real-World Example**: Deciding between a FastAPI/Postgres stack or a Serverless Lambda approach based on the PRD.
*   **Workflow**: `@[/ai-system-design]`
*   **How to Work with it**: Triggers a multi-stage process: ADR creation -> Mermaid diagramming -> API contract definition. The agent will ask for validation at each architectural pivot.
*   **Gate Artifact**: `knowledge/ai-design.md`

### P4: Build (The Flesh)
*   **Why it Matters**: The execution phase where "Intent" becomes "Reality."
*   **Real-World Example**: Writing the actual Python code for the Auth middleware and the accompanying unit tests.
*   **Workflow**: `@[/feature-development]`, `@[/tdd-cycle]`
*   **How to Work with it**: The core of daily work. Use `/feature-development` for standard cycles. For complex logic, switch to `/tdd-cycle` to ensure high test coverage from the start.
*   **Pattern**: `Red (Fail) -> Green (Pass) -> Refactor -> Walkthrough`.

### P5: Test & Eval (The Mirror)
*   **Why it Matters**: Prove that the implementation matches the requirements (Verifiability).
*   **Real-World Example**: Running a load test on the new API and an LLM-based evaluation on the agent's response accuracy.
*   **Workflow**: `@[/agent-testing]`, `@[/quality-gate]`
*   **How to Work with it**: Run `/agent-testing` to execute the full suite. If it fails, the agent will provide a "Debugger's Perspective" and suggest specific fixes. `/quality-gate` is often tied to pre-merge hooks.
*   **Gate Artifact**: `knowledge/eval-report.md`

### P6: Deploy (The Birth)
*   **Why it Matters**: Safely delivering the value to the stakeholders (Love/Service).
*   *Real-World Example**: Merging the feature branch into main, tagging `v2.1.0`, and generating release documentation.
*   **Workflow**: `@[/release-management]`, `@[/documentation-workflow]`
*   **How to Work with it**: Use `/release-management` to bump versions and generate changelogs. Use `/documentation-workflow` to ensure all cross-references across the repo are synchronized (e.g., updating the workflow catalog).

### P7: Monitor (The Pulse)
*   **Why it Matters**: Ensures long-term health and triggers the next cycle of improvement.
*   **Real-World Example**: Tracking error rates in production and discovering that users need a specific UI filter—feeding back into P1.
*   **Workflow**: `@[/monitor]`
*   **How to Work with it**: Configures telemetry and sets up basic health checks. The output feeds back into the backlog, potentially triggering a new P1 cycle for improvements.

---

## Developer Experience (DX)

### Triggering Workflows
You can interact with the SDLC through two primary channels:
1.  **IDE (Slash Commands)**: Type `/` in the agentic UI to see all available workflows. Recommended for interactive dev loops.
2.  **CLI (Automation)**: Use `python cli/factory_cli.py --workflow <name>` for batch processing and CI/CD triggers.

### Environment Context
*   **Core**: Python 3.12+ (managed via Conda: `cursor-factory`).
*   **Infrastructure**: Qdrant (RAG), Postgres (Plane), and Docker for environment isolation.
*   **Safety**: The **Guardian** monitors the shell and API calls in real-time.

---

## Best Practices
- **Atomic Commits**: Link every commit to a Phase Gate or Plane issue.
- **Evidence-First**: Always include screenshots, terminal logs, or recordings in your `walkthrough.md`.
- **Axiomatic Alignment**: If a requirement feels "wrong," trigger a `@[/review-requirements]` session immediately.
- **No Stubs**: Documentation must be high-fidelity. Avoid placeholder "TBD" sections.

## Related Resources
- [Architecture Overview](../architecture/architecture-overview.md) - System context and C4 diagrams.
- [Axiomatic Principles](../architecture/axiomatic-principles.md) - Philosophy and L0 logic.
- [Workflow Catalog](../reference/catalog.md) - Full list of executable paths.

---
*Last Updated: March 2026*
