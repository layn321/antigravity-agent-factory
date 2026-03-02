"""
Central LLM & Embedding Model Configuration Loader.

Single source of truth for all model identifiers used across the factory.
Reads from config/llm_config.json at project root. Falls back to
hardcoded defaults if the config file is missing.

Usage:
    from scripts.ai.llm_config import get_primary_model, get_embedding_model

    llm = ChatGoogleGenerativeAI(model=get_primary_model(), temperature=get_temperature())
"""

import json
import os
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

# ─── Hardcoded Defaults (used only when config file is missing) ───────────────

_DEFAULTS = {
    "llm": {
        "primary_model": "gemini-2.5-flash",
        "fallback_model": "gemini-2.5-flash-lite",
        "preview_model": "gemini-3-flash-preview",
        "default_temperature": 0.0,
    },
    "embedding": {
        "model": "sentence-transformers/all-MiniLM-L6-v2",
        "dimension": 384,
    },
}

# ─── Config Loading ───────────────────────────────────────────────────────────

_CONFIG_PATH = os.path.join(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")),
    "config",
    "llm_config.json",
)

_config: Dict[str, Any] = {}


def _load_config() -> Dict[str, Any]:
    """Load config from disk, falling back to defaults."""
    global _config
    if _config:
        return _config

    if os.path.exists(_CONFIG_PATH):
        try:
            with open(_CONFIG_PATH, "r", encoding="utf-8") as f:
                _config = json.load(f)
            logger.info(f"Loaded LLM config from {_CONFIG_PATH}")
        except Exception as e:
            logger.warning(f"Failed to load {_CONFIG_PATH}: {e}. Using defaults.")
            _config = _DEFAULTS.copy()
    else:
        logger.info(
            f"LLM config not found at {_CONFIG_PATH}. Using hardcoded defaults."
        )
        _config = _DEFAULTS.copy()

    return _config


def reload_config() -> Dict[str, Any]:
    """Force reload of config from disk."""
    global _config
    _config = {}
    return _load_config()


# ─── Public Accessors ─────────────────────────────────────────────────────────


def get_llm_config() -> Dict[str, Any]:
    """Return the full LLM configuration dict."""
    cfg = _load_config()
    return cfg.get("llm", _DEFAULTS["llm"])


def get_primary_model() -> str:
    """Primary LLM model identifier (e.g. 'gemini-2.5-flash')."""
    return get_llm_config().get("primary_model", _DEFAULTS["llm"]["primary_model"])


def get_fallback_model() -> str:
    """Fallback LLM model identifier (e.g. 'gemini-2.5-flash-lite')."""
    return get_llm_config().get("fallback_model", _DEFAULTS["llm"]["fallback_model"])


def get_preview_model() -> str:
    """Preview/experimental LLM model identifier."""
    return get_llm_config().get("preview_model", _DEFAULTS["llm"]["preview_model"])


def get_temperature() -> float:
    """Default LLM temperature."""
    return float(
        get_llm_config().get(
            "default_temperature", _DEFAULTS["llm"]["default_temperature"]
        )
    )


def get_embedding_config() -> Dict[str, Any]:
    """Return the full embedding configuration dict."""
    cfg = _load_config()
    return cfg.get("embedding", _DEFAULTS["embedding"])


def get_embedding_model() -> str:
    """Embedding model identifier (e.g. 'sentence-transformers/all-MiniLM-L6-v2')."""
    return get_embedding_config().get("model", _DEFAULTS["embedding"]["model"])


def get_embedding_dimension() -> int:
    """Embedding vector dimension (e.g. 384 for MiniLM)."""
    return int(
        get_embedding_config().get("dimension", _DEFAULTS["embedding"]["dimension"])
    )
