import json
import hashlib
import os
import time
from typing import Any, Callable, Dict, Optional, Union
from datetime import datetime

# Logic for Memory MCP integration (conceptual or via subprocess if needed)
# Since the agent environment uses MCP tools, this script serves as a
# standard logic provider for skills that want to implement memoization.

CACHE_FILE = ".agent/knowledge/tool-cache.json"


class Memoizer:
    """
    A persistent memoization system for deterministic tool calls.
    Integrates with the Factory's Hybrid Memory Architecture.
    """

    def __init__(self, use_memory_mcp: bool = True, persistence_file: str = CACHE_FILE):
        self.use_memory_mcp = use_memory_mcp
        self.persistence_file = persistence_file
        self._ensure_cache_dir()

    def _ensure_cache_dir(self):
        os.makedirs(os.path.dirname(self.persistence_file), exist_ok=True)
        if not os.path.exists(self.persistence_file):
            with open(self.persistence_file, "w") as f:
                json.dump({}, f)

    def _generate_key(self, tool_name: str, args: Dict[str, Any]) -> str:
        """Generates a unique hash for a tool call."""
        arg_str = json.dumps(args, sort_keys=True)
        return hashlib.sha256(f"{tool_name}:{arg_str}".encode()).hexdigest()

    def get_cached_result(self, tool_name: str, args: Dict[str, Any]) -> Optional[Any]:
        """
        In a real implementation, this would query the Memory MCP 'Episodic'
        observations first, then the local JSON cache.
        """
        key = self._generate_key(tool_name, args)

        # 1. Check local JSON cache (Semantic/Persistent)
        try:
            with open(self.persistence_file, "r") as f:
                cache = json.load(f)
                if key in cache:
                    # Check TTL if implemented
                    entry = cache[key]
                    if "expires_at" not in entry or entry["expires_at"] > time.time():
                        return entry["result"]
        except Exception:
            pass

        return None

    def cache_result(
        self, tool_name: str, args: Dict[str, Any], result: Any, ttl: int = 3600 * 24
    ):
        """Stores a result in the persistent cache."""
        key = self._generate_key(tool_name, args)
        expires_at = time.time() + ttl

        try:
            with open(self.persistence_file, "r") as f:
                cache = json.load(f)

            cache[key] = {
                "tool": tool_name,
                "args": args,
                "result": result,
                "cached_at": datetime.now().isoformat(),
                "expires_at": expires_at,
            }

            with open(self.persistence_file, "w") as f:
                json.dump(cache, f, indent=2)
        except Exception:
            pass


def memoize_tool(ttl: int = 86400):
    """
    Decorator for tool functions to enable memoization.
    Note: In the agentic context, this is a pattern to be used by skill implementations.
    """

    def decorator(func: Callable):
        memoizer = Memoizer()

        def wrapper(*args, **kwargs):
            # Convert args/kwargs to a single dict for hashing
            # (Simplified for the demonstration)
            tool_args = kwargs
            cached = memoizer.get_cached_result(func.__name__, tool_args)
            if cached is not None:
                return cached

            result = func(*args, **kwargs)
            memoizer.cache_result(func.__name__, tool_args, result, ttl)
            return result

        return wrapper

    return decorator
