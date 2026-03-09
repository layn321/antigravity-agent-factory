# Agent Coordination & Topological Patterns

This document defines the strategic orchestration and tactical coordination patterns used by the Antigravity Agent Factory.

## 🏛️ Strategic Orchestration: The MSO

The **Master System Orchestrator (MSO)** is the supreme command entity responsible for strategic decomposition.

- **Objective**: To break down high-level user goals into actionable, parallelizable tasks.
- **Core Workflow**: `/master-system-orchestration`
- **Logic**:
    1. **Decomposition**: Analyze the objective and extract independent sub-tasks.
    2. **Staffing**: Match sub-tasks to functional Specialists using `agent-staffing.json`.
    3. **Orchestration**: Manage the execution flow (Sequential vs. Parallel).

## 👥 Persona-to-Specialist Mapping

Cognitive personas (@Architect, etc.) route to functional specialists for deep domain execution.

| Persona | Specialist | Focus |
| :--- | :--- | :--- |
| **@Architect** | **SYARCH** | Structural integrity and 5-Layer design. |
| **@Bug-Hunter** | **WQSS** | Diagnostics, RCA, and TDD enforcement. |
| **@Documentarian** | **KNOPS** | Knowledge evolution and referential truth. |
| **@Operator** | **PROPS** | Environment stability and project delivery. |

## 🕸️ Topological Patterns

The Factory uses specialized topologies to optimize for speed, accuracy, or creativity.

### 1. Chain (Sequential)
- **Use when**: Task B depends on the output of Task A.
- **Pattern**: `Input -> Agent A -> Agent B -> Output`
- **Example**: Requirements Analysis -> Architecture Design.

### 2. Parallel (Standard)
- **Use when**: Multiple independent tasks can be executed simultaneously.
- **Pattern**: `Input -> [Agent A, Agent B, Agent C] -> Aggregator -> Output`
- **Example**: Creating separate components/files for a single feature.

### 3. Evaluator-Optimizer (Quality)
- **Use when**: High-fidelity output is critical and requires adversarial refinement.
- **Pattern**: `Input -> Generator -> Evaluator (Adversarial) -> Optimizer -> Output`
- **Example**: `/code-review` or `/bugfix-resolution`.

### 4. Multi-Agent Debate (MAD)
- **Use when**: Resolving architectural disputes or complex logic trade-offs.
- **Pattern**: `Agent A (Pro) vs. Agent B (Con) -> Judge (Consensus) -> Decision`
- **Example**: Selecting a database engine or refactoring a core API.

## 🔄 Interaction Protocols

### Reflection Gate
- **Purpose**: To force a pause and verification before irreversible actions.
- **Trigger**: Any non-trivial modification to the core architecture.
- **Action**: Generate `implementation_plan.md` and wait for `@Architect` approval.

---

> [!NOTE]
> These patterns are registered in `.agent/patterns/` and enforced by the `workflow-execution` skill.
