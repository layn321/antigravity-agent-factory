#!/usr/bin/env python
"""
get_rag_toc.py — Retrieve the Table of Contents for a document from the RAG system.

Primary path: Direct invocation of OptimizedRAG.get_toc() (no server required).
Fallback path: MCP SSE server at http://127.0.0.1:8000/sse (if direct import fails).

Usage:
    conda run -p D:\\Anaconda\\envs\\cursor-factory python get_rag_toc.py "Russell"
"""

import sys
import os
import json
import warnings
import logging

# Suppress noisy warnings
warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.WARNING, stream=sys.stderr)

# Force stdout to UTF-8 to prevent Windows cp1252 console crashes
if sys.platform == "win32":
    import io

    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

# Ensure project root is on path
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../../../../")
)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

SERVER_URL = "http://127.0.0.1:8000/sse"


def get_toc_direct(document_name: str) -> dict:
    """Primary path: call OptimizedRAG directly without any server dependency."""
    from scripts.ai.rag.rag_optimized import OptimizedRAG

    rag = OptimizedRAG(warmup=True)
    toc = rag.get_toc(document_name)

    if toc:
        return {"toc": toc}
    else:
        return {"toc": None, "error": f"No TOC found for '{document_name}'."}


async def get_toc_via_mcp(document_name: str) -> dict:
    """Fallback path: call via MCP SSE server (requires server to be running)."""
    from langchain_mcp_adapters.client import MultiServerMCPClient

    client = MultiServerMCPClient(
        connections={"rag_server": {"url": SERVER_URL, "transport": "sse"}}
    )

    tools = await client.get_tools()
    toc_tool = next((t for t in tools if t.name == "get_ebook_toc"), None)

    if toc_tool:
        result = await toc_tool.ainvoke({"document_name": document_name})
        return result if isinstance(result, (dict, list)) else {"toc": str(result)}
    else:
        return {"error": "'get_ebook_toc' tool not found on server."}


def main():
    if len(sys.argv) < 2:
        print(
            'Usage: python get_rag_toc.py "<document_name_or_keyword>"',
            file=sys.stderr,
        )
        sys.exit(1)

    doc_name = sys.argv[1]

    # Strategy 1: Direct OptimizedRAG (preferred — no server needed)
    try:
        result = get_toc_direct(doc_name)
        print(json.dumps(result, ensure_ascii=False))
        return
    except Exception as e:
        print(f"Direct RAG path failed ({e}), trying MCP fallback...", file=sys.stderr)

    # Strategy 2: MCP SSE server fallback
    try:
        import asyncio

        result = asyncio.run(get_toc_via_mcp(doc_name))
        print(json.dumps(result, ensure_ascii=False))
    except Exception as e:
        print(f"Error: Both direct and MCP paths failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
