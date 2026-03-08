import unittest
from unittest.mock import patch, MagicMock
import json
import os
from scripts.core.fetch_telemetry import fetch_telemetry, save_telemetry


class TestFetchTelemetry(unittest.TestCase):
    def test_fetch_telemetry_structure(self):
        traces = fetch_telemetry(agent_id="test-agent", limit=1)
        self.assertEqual(len(traces), 1)
        self.assertEqual(traces[0]["agent_id"], "test-agent")
        self.assertIn("trace_id", traces[0])
        self.assertIn("token_usage", traces[0])

    @patch("scripts.core.fetch_telemetry.Path.mkdir")
    @patch("builtins.open", new_callable=unittest.mock.mock_open)
    def test_save_telemetry(self, mock_file, mock_mkdir):
        traces = [{"trace_id": "123", "data": "test"}]
        save_telemetry(traces, "mock_dir")
        mock_mkdir.assert_called()
        mock_file.assert_called_with(unittest.mock.ANY, "w")


if __name__ == "__main__":
    unittest.main()
