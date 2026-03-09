# IDX Integration Guide: Antigravity IDE UI Optimization

This guide explains how to leverage Antigravity-specific UI features to enhance the developer experience.

## 1. Visual Workflow Builder
Antigravity supports a canvas-based view of `.agent/workflows/*.md`.
- **How to Use**: Open any workflow file. Look for the "Visual Mode" or "Flowchart" icon in the top-right toolbar.
- **Optimization**: Use mermaid diagrams within the markdown to hint the IDE's renderer on how to connect nodes.

## 2. Live Thought Trace
The IDE can stream internal `sequentialthinking` steps in real-time.
- **How to Use**: Toggle the "Thought Trace" panel in the Agent View settings.
- **Optimization**: Clearly label your thought numbers and use `is_revision` when changing plans to give the user a clear "Nudge" opportunity.

## 3. Integrated MCP Manager
View and debug MCP servers without editing `mcp_config.json`.
- **How to Use**: Naviate to the "Manage MCP Servers" view in the IDE's side panel.
- **Optimization**: Ensure all servers have descriptive names and icons for quick identification.

---

## 4. Best Practices for High-Fidelity UI
- **Artifact Hot-Reloading**: Keep `task.md` open in a split pane. The IDE will automatically refresh the view as I call `replace_file_content`.
- **Persona Shortcuts**: Use `@persona` in the chat to trigger specific UI themes or toolsets (e.g., `@Bug-Hunter` activates diagnostic tools).
