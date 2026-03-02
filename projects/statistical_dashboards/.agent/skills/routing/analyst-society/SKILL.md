# Skill: Analyst Society Coordination

## Overview
The 'Analyst Society' is a multi-agent coordination pattern designed to handle complex, multi-disciplinary analytical tasks. It uses a **Supervisor** to coordinate between specialized **Workers**.

## Architectural Pattern
- **Supervisor**: The central router and decision-maker. It maintains the global state and delegates tasks to workers based on their expertise.
- **SQL Worker**: Specialized in data retrieval and schema discovery.
- **Statistical Worker**: Specialized in data exploration, visualization, and ML modeling (using dashboard workflows).

## Coordination Logic (LangGraph)
1. **Receive User Query**: The Supervisor analyzes the intent.
2. **Delegate**:
   - If data is needed: Call **SQL Worker**.
   - If analysis/visualization is needed: Call **Statistical Worker**.
3. **Verify**: The Supervisor reviews worker output for completeness and fidelity.
4. **Finalize**: The Supervisor compiles the final response or report.

## Standard State Schema
```python
from typing import TypedDict, Annotated, List, Union
from pydantic import BaseModel, Field

class AnalystState(TypedDict):
    query: str
    data_context: str
    analytical_findings: List[str]
    current_worker: str
    iteration_count: int
    final_output: str
```

## Discovery
Use `mcp_plane_list_work_items` to identify analytical tasks and `mcp-fetch` to source external data for the Analyst Society.
