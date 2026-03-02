---
name: managing-plane-tasks
description: Remote management of Plane PMS issues and states using the Plane MCP server.
type: skill
version: 2.0.0
category: routing
agents:
- python-ai-specialist
- ai-app-developer
- master-system-orchestrator
knowledge:
- plane-integration.json
- api-integration-patterns.json
tools:
- mcp_plane_list_work_items
- mcp_plane_create_work_item
- mcp_plane_update_work_item
- mcp_plane_retrieve_work_item
- mcp_plane_list_labels
- mcp_plane_create_label
- mcp_plane_list_states
- mcp_plane_list_cycles
- mcp_plane_list_modules
- mcp_plane_get_me
related_skills:
- orchestrating-mcp
- mastering-project-management
templates:
- ["none"]
---

# Remote Plane Management (MCP)

This skill enables agents to manage projects, issues, and states in a remote Plane PMS instance using the **Plane MCP server**. This is the primary and recommended method for all project management operations, replacing the legacy local management scripts.

## When to Use
- When you need to create, update, or track tasks in the hosted Plane instance.
- For all standard project lifecycle automation (refinement, updates, reporting).
- When a pure, standardized, and machine-readable interface is required for agentic workflows.

## Prerequisites
- **Plane MCP Server**: Must be active and configured in `mcp_config.json`.
- **Project Context**: Project ID (e.g., `e71eb003-87d4-4b0c-a765-a044ac5affbe`) and Identifier (e.g., `AGENT`) must be provided.
- **Label Synchronization**: Always adhere to the project's global [Label Governance](file:///d:/Users/wpoga/Documents/Python%20Scripts/antigravity-agent-factory/.agent/skills/chain/mastering-project-management/SKILL.md#label-governance-source-of-truth).

## Process

Follow this end-to-end workflow for all Plane project management operations.

### 1. Listing & Discovery
Use `mcp_plane_list_work_items` with appropriate filtering. Prefer `expand` for full metadata.

```json
// Tool: mcp_plane_list_work_items
{
  "project_id": "e71eb003-87d4-4b0c-a765-a044ac5affbe",
  "expand": "labels,state,assignees",
  "order_by": "-updated_at"
}
```

### 2. Detailed Inspection
Retrieve the full details of a specific item, including description and comments.

```json
// Tool: mcp_plane_retrieve_work_item
{
  "project_id": "e71eb003-87d4-4b0c-a765-a044ac5affbe",
  "work_item_id": "UUID-OR-IDENTIFIER"
}
```

### 3. Professional Task Creation (Mandatory Workflow)

A work item is **NOT considered created** until ALL mandatory properties are set. Agents MUST execute Steps A through D in sequence. **No exceptions.**

> [!CAUTION]
> Creating a work item without start_date, target_date, estimate, labels, module, and cycle is a governance violation. Always complete the full workflow.

#### Pre-Flight Checklist
Before calling `mcp_plane_create_work_item`, resolve ALL of the following:

| Property | How to Resolve | Required |
| :--- | :--- | :---: |
| `labels` | `mcp_plane_list_labels` → pick 1+ label UUIDs | ✅ |
| `assignees` | `mcp_plane_get_me` → use your own UUID | ✅ |
| `state` | `mcp_plane_list_states` → pick initial state (usually Todo) | ✅ |
| `start_date` | ISO 8601 date (e.g., `"2026-03-02"`) | ✅ |
| `target_date` | ISO 8601 date (e.g., `"2026-03-08"`) | ✅ |
| `estimate_point` | Use project estimate scale UUID | ✅ |
| `parent` | If item belongs to an Epic, set the Epic's work item UUID | ⚠️ If applicable |
| Module | Resolved in Step B | ✅ |
| Cycle | Resolved in Step C | ✅ |

#### Step A: Full Issue Creation
Create the issue with **all** core metadata in a single call.

```json
// Tool: mcp_plane_create_work_item
{
  "project_id": "e71eb003-87d4-4b0c-a765-a044ac5affbe",
  "name": "FEATURE: Implement Multi-Agent 'Analyst Society' for Dashboards",
  "description_html": "<div>Develop a LangGraph-based multi-agent coordination flow...</div>",
  "priority": "high",
  "state": "8e155185-58ad-404b-8458-6a7c9edbf09b",
  "assignees": ["e559df98-fc43-4578-a3e0-3b77e3b35bc4"],
  "labels": ["57a1da51-90c6-46db-9340-6c88ac9b1ed0"],
  "start_date": "2026-03-02",
  "target_date": "2026-03-08",
  "estimate_point": "a1f66f54-0f4b-4ca1-9979-a34087b4594a",
  "parent": "EPIC-UUID-IF-APPLICABLE"
}
```

#### Step B: Mandatory Module Association (exactly 1 module)

```json
// Tool: mcp_plane_add_work_items_to_module
{
  "project_id": "e71eb003-87d4-4b0c-a765-a044ac5affbe",
  "module_id": "a4123817-7b59-474a-b4d2-7d0fcb3d3fc9",
  "issue_ids": ["NEW-ISSUE-UUID"]
}
```

#### Step C: Mandatory Cycle Association

```json
// Tool: mcp_plane_add_work_items_to_cycle
{
  "project_id": "e71eb003-87d4-4b0c-a765-a044ac5affbe",
  "cycle_id": "ACTIVE-CYCLE-UUID",
  "issue_ids": ["NEW-ISSUE-UUID"]
}
```

#### Step D: Epic Linking (When Applicable)
If the work item is a sub-task of a larger Epic, set the `parent` field during Step A. If the Epic UUID was not known at creation time, update it immediately:

```json
// Tool: mcp_plane_update_work_item
{
  "project_id": "e71eb003-87d4-4b0c-a765-a044ac5affbe",
  "work_item_id": "NEW-ISSUE-UUID",
  "parent": "EPIC-PARENT-UUID"
}
```

### 4. Updating Status & Metadata
Move issues through the lifecycle by updating the `state` or adding professional progress reports.

```json
// Tool: mcp_plane_update_work_item
{
  "project_id": "e71eb003-87d4-4b0c-a765-a044ac5affbe",
  "work_item_id": "ITEM-UUID",
  "state": "ef4b2395-3edb-41e9-adcd-7ec77d534f0f" // Done UUID
}
```

## Label Governance (Source of Truth)

All labeling must strictly follow the synchronized set:
- `BUG`, `CORE`, `DATA`, `DOCU`, `FEATURE`, `TEST`, `UI`
- `ORCHESTRATION`, `GROUNDING`, `INTEGRATION`, `INFRA`, `SKILL`

> [!IMPORTANT]
> Use `mcp_plane_list_labels` to verify available labels and their IDs before creating or updating work items.

## Professional Documentation Standards
When closing issues, provide a detailed summary of the accomplishment:
- **Technical Summary**: High-level problem and solution.
- **Files Affected**: Key modules modified.
- **Verification Proof**: Test results and coverage details.
- **Future Prevention**: Added guards or scripts.

## Best Practices
- **Always resolve metadata first**: Use `mcp_plane_list_labels`, `mcp_plane_list_states`, `mcp_plane_get_me` before creating work items to ensure valid UUIDs.
- **Complete the full workflow**: A work item is not finished until it has labels, assignee, state, dates, module, and cycle attached (Steps A–D).
- **Use expand for context**: When listing or retrieving items, use `expand: "labels,state,assignees"` to get full metadata in one call.
- **Never hardcode UUIDs**: Always query for the current label/state/cycle IDs; they may change between environments.
- **Document closures professionally**: When marking items Done, add a comment with technical summary, files affected, and verification proof.
- **Respect label governance**: Only use labels from the synchronized set. Run `mcp_plane_list_labels` to verify before tagging.

---
*Operational maturity is the foundation of high-velocity agency.*
