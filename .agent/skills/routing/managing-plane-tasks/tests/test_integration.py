import os
import sys
import json
import time
import requests
import unittest

# Add the scripts directory to sys.path so we can import create_task
SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(SKILL_ROOT, "scripts")
sys.path.insert(0, SCRIPTS_DIR)

import create_task


class TestPlaneIntegration(unittest.TestCase):
    """
    Integration tests for Plane API.
    These tests hit the real API and create/delete a task.
    They should be run manually, not in CI/CD.
    """

    @classmethod
    def setUpClass(cls):
        # Ensure API key is present
        if not os.environ.get("PLANE_API_TOKEN"):
            raise unittest.SkipTest(
                "PLANE_API_TOKEN not set. Skipping integration tests."
            )

        cls.workspace = create_task.WORKSPACE_SLUG
        cls.project_id = create_task.PROJECT_ID
        cls.api_base = create_task.API_BASE
        cls.headers = {
            "x-api-key": os.environ.get("PLANE_API_TOKEN"),
            "Content-Type": "application/json",
        }

        # Test payload
        cls.test_payload = {
            "name": "[TEST] Integration Test Task",
            "type": "test",
            "requirements": ["Must be created", "Must be deleted"],
            "acceptance_criteria": ["It works"],
            "workflows": [],
            "agents": [],
            "skills": [],
            "tests": [],
            "labels": ["TEST"],
        }

    def test_create_and_delete_task(self):
        """End-to-End test: Create a task, verify it exists, then delete it."""
        try:
            # 1. Load Data
            tmp_path = os.path.join(SCRIPTS_DIR, "tmp_integration_input.json")
            with open(tmp_path, "w", encoding="utf-8") as f:
                json.dump(self.test_payload, f)

            data = create_task.load_input(tmp_path)

            # 2. Render Template
            html = create_task.render_template(data)
            self.assertIn("<h3>📋 Requirements</h3>", html)

            # 3. Create Task
            print("\n[Integration] Creating task...")
            result = create_task.create_work_item(data, html)

            self.assertIsNotNone(result)
            self.assertIn("id", result)

            task_id = result["id"]
            seq_id = result.get("sequence_id")
            print(f"[Integration] Task Created: AGENT-{seq_id} (ID: {task_id})")

            # Allow a short delay for Plane to index
            time.sleep(2)

            # 4. Verify Task Exists
            print(f"[Integration] Verifying task AGENT-{seq_id}...")
            get_url = f"{self.api_base}/work-items/{task_id}/"
            resp = requests.get(get_url, headers=self.headers)
            self.assertEqual(resp.status_code, 200, "Failed to fetch created task")

            fetched_data = resp.json()
            self.assertEqual(fetched_data["name"], self.test_payload["name"])

            # 5. Delete Task
            print(f"[Integration] Deleting task AGENT-{seq_id}...")
            delete_url = f"{self.api_base}/work-items/{task_id}/"
            del_resp = requests.delete(delete_url, headers=self.headers)

            self.assertEqual(
                del_resp.status_code, 204, f"Failed to delete task: {del_resp.text}"
            )
            print(f"[Integration] Successfully deleted task AGENT-{seq_id}")

        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)


if __name__ == "__main__":
    # Add a note that this requires the API token
    print("Running Plane Integration Tests...")
    print("WARNING: This will create and delete real issues in Plane.")
    unittest.main()
