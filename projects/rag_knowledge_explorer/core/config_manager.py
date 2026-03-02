import os
import json
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class ConfigManager:
    """
    Centralized configuration manager for the Standalone RAG Knowledge Explorer.
    """

    @staticmethod
    def _get_factory_defaults():
        """Load defaults from factory-level config/llm_config.json."""
        try:
            import sys

            factory_root = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "../../../")
            )
            if factory_root not in sys.path:
                sys.path.insert(0, factory_root)
            from scripts.ai.llm_config import get_llm_config

            return get_llm_config()
        except Exception:
            # Fallback if factory config unavailable
            return {
                "primary_model": "gemini-2.5-flash",
                "preview_model": "gemini-3-flash-preview",
                "fallback_model": "gemini-2.5-flash-lite",
                "default_temperature": 0.0,
            }

    DEFAULT_LLM_CONFIG = _get_factory_defaults.__func__()

    def __init__(self):
        # Path is relative to this file's location in core/
        self._project_root = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../")
        )
        self._config_file = os.path.join(self._project_root, "config", "settings.json")
        self._config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        if not os.path.exists(self._config_file):
            logger.info(
                f"Config file not found at {self._config_file}. Using defaults."
            )
            os.makedirs(os.path.dirname(self._config_file), exist_ok=True)
            return {"llm": self.DEFAULT_LLM_CONFIG}

        try:
            with open(self._config_file, "r") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading config file: {e}")
            return {"llm": self.DEFAULT_LLM_CONFIG}

    def get_llm_config(self) -> Dict[str, Any]:
        return self._config.get("llm", self.DEFAULT_LLM_CONFIG)


config_manager = ConfigManager()
