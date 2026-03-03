import os
import sys
import json
import unittest
from unittest.mock import patch, MagicMock

# Add the scripts directory to sys.path so we can import create_task
SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(SKILL_ROOT, "scripts")
sys.path.insert(0, SCRIPTS_DIR)

import create_task


class TestCreateTask(unittest.TestCase):
    def setUp(self):
        self.sample_data = {
            "name": "Test Task",
            "type": "feature",
            "requirements": ["Req 1", "Req 2"],
            "acceptance_criteria": ["Crit 1", "Crit 2"],
            "estimate": "5 points",
            "module_name": "Core System",
            "cycle_name": "Sprint 42",
            "parent_name": "Epic Alpha",
            "start_date": "2026-03-03",
            "target_date": "2026-03-10",
            "workflows": ["workflow-a"],
            "agents": ["agent-x"],
            "skills": ["skill-y"],
            "tests": [{"type": "unit", "script": "test.py", "expected": "pass"}],
            "rules": ["rule-z"],
            "priority": "high",
            "labels": ["FEATURE"],
        }

    def test_load_input_defaults(self):
        """Test that load_input sets the correct default values for missing fields."""
        # Create a temporary JSON file
        tmp_path = os.path.join(SCRIPTS_DIR, "tmp_test_input.json")
        try:
            with open(tmp_path, "w", encoding="utf-8") as f:
                json.dump(self.sample_data, f)

            data = create_task.load_input(tmp_path)

            # Check defaults
            self.assertEqual(data["patterns"], [])
            self.assertEqual(data["blueprints"], [])
            self.assertEqual(data["templates"], [])
            self.assertEqual(data["knowledge"], [])
            self.assertEqual(data["scripts"], [])
            self.assertEqual(data["memory_queries"], [])
            self.assertEqual(data["notes"], "")
            self.assertEqual(data["priority"], "high")  # Preserved from input
            self.assertEqual(data["labels"], ["FEATURE"])  # Preserved from input

        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def test_render_template(self):
        """Test that the Jinja template renders correctly with provided data."""
        html = create_task.render_template(self.sample_data)

        # Check basic structural elements
        self.assertIn("<h3>📋 Requirements</h3>", html)
        self.assertIn("<li>Req 1</li>", html)
        self.assertIn("<li>Req 2</li>", html)

        self.assertIn("<h3>✅ Acceptance Criteria</h3>", html)
        self.assertIn("Crit 1", html)

        self.assertIn("<h3>🏭 Factory Asset Assignment</h3>", html)
        self.assertIn("<strong>🔄 Workflows:</strong>", html)
        self.assertIn("<code>workflow-a</code>", html)
        self.assertIn("<strong>👤 Agents:</strong>", html)
        self.assertIn("<code>agent-x</code>", html)
        self.assertIn("<strong>🧩 Skills:</strong>", html)
        self.assertIn("<code>skill-y</code>", html)
        self.assertIn("<strong>📏 Rules:</strong>", html)
        self.assertIn("<code>rule-z</code>", html)

        self.assertIn("<h3>🧪 Test Strategy</h3>", html)
        self.assertIn("<strong>[UNIT]</strong>", html)
        self.assertIn("<code>test.py</code>", html)
        self.assertIn("pass", html)

    @patch("os.path.isdir")
    @patch("os.listdir")
    def test_check_artifacts_exist_missing(self, mock_listdir, mock_isdir):
        """Test the continuous improvement loop detects missing artifacts."""
        # Setup mocks to simulate an empty repository
        mock_isdir.return_value = True
        mock_listdir.return_value = []

        data = {
            "workflows": ["feature-development"],
            "skills": ["[NEW] new-skill", "missing-skill"],
        }

        missing = create_task.check_artifacts_exist(data)

        # Should flag missing workflows and skills, including the explicit [NEW] tag
        missing_dict = {(m["type"], m["name"]) for m in missing}

        self.assertIn(("workflows", "feature-development"), missing_dict)
        self.assertIn(("skills", "new-skill"), missing_dict)
        self.assertIn(("skills", "missing-skill"), missing_dict)

    @patch("os.path.isdir")
    @patch("os.listdir")
    def test_check_artifacts_exist_found(self, mock_listdir, mock_isdir):
        """Test that existing artifacts are not flagged as missing."""
        # Setup mocks to simulate existing artifacts
        mock_isdir.return_value = True

        def simulated_listdir(path):
            if "workflows" in path:
                return ["feature-development.md"]
            elif "skills" in path:
                return ["existing-skill"]
            return []

        mock_listdir.side_effect = simulated_listdir

        data = {"workflows": ["feature-development"], "skills": ["existing-skill"]}

        missing = create_task.check_artifacts_exist(data)
        self.assertEqual(len(missing), 0)

    @patch("requests.get")
    def test_get_label_map(self, mock_get):
        """Test dynamic label fetching from Plane API."""
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "results": [
                {"name": "Feature", "id": "uuid-1"},
                {"name": "BUG", "id": "uuid-2"},
            ]
        }
        mock_get.return_value = mock_resp

        label_map = create_task.get_label_map({"x-api-key": "test"})

        self.assertEqual(label_map["FEATURE"], "uuid-1")
        self.assertEqual(label_map["BUG"], "uuid-2")


if __name__ == "__main__":
    unittest.main()
