---
name: mastering-project-management
description: Procedural truth for orchestrating high-fidelity software delivery via Plane MCP server.
type: skill
version: 2.0.0
category: chain
---

# Capability Manifest: Project Management Mastery

This blueprint provides the **procedural truth** for orchestrating high-fidelity software delivery. The key is to use the **Plane MCP server** for all remote operations (Issue creation, label management, state updates) and standardized naming conventions to ensure the project remains high-fidelity and machine-readable.

## When to Use

This skill should be used when completing tasks related to project management mastery.

## Process

Follow these procedures to implement the capability:

### Procedure 1: Backlog Excellence (Refinement)
1.  **Definition of Ready (DoR)**: A story is only ready when it has:
    - **Persona-based Description**: Clear "As a... I want... So that..." or structured **# Goal** header.
    - **3+ Clear Acceptance Criteria (AC)**: Explicit validation steps.
    - **Link to a parent Epic**: Or appropriate Module/Cycle categorization.
    - **Estimation (Points/Hours)**: Every task must have an estimate.
    - **Technical Context**: Implementation notes to guide the developer agent.
2.  **MoSCoW Prioritization**: Mandatory tags for every story:
    - `Must`: Essential for the next release.
    - `Should`: Important but not critical.
    - `Could`: Nice to have.
    - `Won't`: Deferred.

### Procedure 2: Sprint Orchestration (Flow)
1.  **Capacity Gate**: Before starting a sprint, run `pm.calculateVelocity()` and verify against the proposed total points.
2.  **State Transitions**: Enforce strict flow: `To Do` -> `In Progress` -> `In Review` -> `Verification` -> `Done`.
3.  **Blocker Management**: Any item in `In Progress` for >40% of sprint length must be flagged as `AT_RISK` and requires a mitigation comment.

### Procedure 3: Reporting & Observability
1.  **Automated Changelog**: Pull all `Done` stories since the last release tag and generate grouped release notes.
2.  **Velocity Tracking**: Generate a CSV/JSON of points completed per sprint to build the "Historical Truth" for planning.
3.  **Stakeholder Sync**: Weekly automated summary of `Must/Should` progress and identified risks.

## Process (Fail-State & Recovery)

| Symptom | Probable Cause | Recovery Operation |
| :--- | :--- | :--- |
| **Silent Sprint Fail** | Scope creep or hidden blockers. | Run a "Sprint Audit" to compare mid-sprint state vs. initial commitment; move non-critical items back to backlog. |
| **Metric Inaccuracy** | Stale status in the PM backend. | Trigger a "Status Refresh" nudge to all active agents; run `pm.syncFromBackend()`. |
| **Story Rejection** | Vague ACs leading to incorrect implementation. | Reject the story; conduct a "Hard Refinement" session to redefine ACs with the developer agent. |

## Prerequisites

| Action | Tool / Command |
| :--- | :--- |
| Create Work Item | `mcp_plane_create_work_item` |
| List Work Items | `mcp_plane_list_work_items` |
| Retrieve Item | `mcp_plane_retrieve_work_item` |
| Update Item | `mcp_plane_update_work_item` |
| Search Items | `mcp_plane_search_work_items` |

## Label Governance (Source of Truth)

Every work item MUST be tagged with at least one label from this synchronized set. For **Remote Plane** operations, always use the `mcp_plane` tools (`create_label`, `update_label`, `list_labels`) to maintain this synchronization. Do NOT use local management scripts for remote label administration.

| Label | Description |
| :--- | :--- |
| `BUG` | Defect or unexpected behavior. |
| `CORE` | Core system infrastructure and logic. |
| `DATA` | Data models, migrations, and pipelines. |
| `DOCU` | Documentation and knowledge items. |
| `FEATURE` | New functional capabilities. |
| `TEST` | Testing infrastructure and test cases. |
| `UI` | User interface and experience. |
| `ORCHESTRATION` | Agent coordination, loops, and supervisor logic. |
| `GROUNDING` | RAG patterns, knowledge retrieval, and memory management. |
| `INTEGRATION` | MCP server connections and external API logic. |
| `INFRA` | Environment setup, Conda, and shell platform management. |
| `SKILL` | Development and refinement of agent skills. |

## Best Practices
Before starting a sprint:
- [ ] Every item meets the Definition of Ready.
- [ ] Total points < 105% of historical velocity.
- [ ] Dependencies map is clear (No circular blocks).
- [ ] Release target is identified and dated.

## Example Library (Recipes)

To ensure excellence, use these copy-pasteable patterns for common scenarios.

### 1. Creating a Standardized Feature
```json
// Tool: mcp_plane_create_work_item
{
  "project_id": "e71eb003-87d4-4b0c-a765-a044ac5affbe",
  "name": "FEATURE: Implement OIDC Authentication Support",
  "priority": "high",
  "description_html": "<div>Develop and integrate OIDC auth flow...</div>",
  "labels": ["5248c180-2056-495c-859c-82747b5d1d52", "5b807a8c-09c4-49d5-ac0d-290568780564"] // FEATURE, CORE
}
```

### 2. Updating Status & Adding Comments
```json
// Tool: mcp_plane_update_work_item
{
  "project_id": "e71eb003-87d4-4b0c-a765-a044ac5affbe",
  "work_item_id": "AGENT-42-UUID",
  "state": "8e155185-58ad-404b-8458-6a7c9edbf09b" // To Do
}

// Tool: mcp_plane_create_work_item_comment
{
  "project_id": "e71eb003-87d4-4b0c-a765-a044ac5affbe",
  "work_item_id": "AGENT-42-UUID",
  "comment_html": "<div>Verification successful. Moving to Production.</div>"
}
```

### 3. Batch Retrieval for Reporting
```json
// Tool: mcp_plane_list_work_items
{
  "project_id": "e71eb003-87d4-4b0c-a765-a044ac5affbe",
  "expand": "assignees,labels,state",
  "order_by": "-updated_at"
}
```

## Troubleshooting & Fail-State
| Symptom | Probable Cause | Recovery Operation |
| :--- | :--- | :--- |
| **Shell Error** (`&` or `|`) | Malformed CLI string. | Use the **Reliability Layer** (`--file`). |
| **Duplicate Blocked** | Issue already exists. | Use `--force` only if intent is truly distinct. |
| **Label Inflation** | Missing governance. | Refer to AGENT-85 Taxonomy (Status: Planned). |

---
*Operational maturity is the foundation of high-velocity agency.*
