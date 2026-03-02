---
description: Automated workflow for facilitating dashboard-specific project planning and status updates.
---

# Dashboard Project Governance

This workflow manages the lifecycle of dashboard-specific issues and status reporting.

## Steps

1. **Backlog Refinement**
   - Review new requirements for the dashboard.
   - Decompose into technical tasks (Data, Logic, UI).

2. **Sprint Execution**
   - Update statuses for AGENT tasks in Plane.
   - Ensure every issue has a "Responsible Person" and Estimation.

3. **Reporting**
   - Execute the `exec-summary` routine to pull status from Plane.
   - Update the `dashboard_status.md` file in project memory.

4. **Finalization**
   - Closure of the cycle/sprint.
   - archival of model artifacts and report publishing.
