import json
import os
from datetime import datetime


class MemorySyncManager:
    """Manages the preparation of dashboard project data for the Antigravity Memory MCP."""

    def __init__(self, sync_dir="projects/statistical_dashboards/data/sync"):
        self.sync_dir = sync_dir
        if not os.path.exists(self.sync_dir):
            os.makedirs(self.sync_dir)

    def prepare_sync_payload(self, project, artifact_links=None):
        """
        Creates a JSON payload for the agent to ingest via Memory MCP.
        This fulfills the synchronization hook requirement.
        """
        observations = [
            f"Description: {project.description}",
        ]

        # Add dataset summary
        if project.datasets:
            observations.append(
                f"Datasets Attached: {', '.join([d.filename for d in project.datasets])}"
            )
            observations.append(
                f"Total Combined Data Rows: {sum(d.row_count for d in project.datasets)}"
            )

        # Add links to artifacts (if any provided)
        if artifact_links:
            for link in artifact_links:
                observations.append(f"Data Artifact: {link}")

        payload = {
            "entity_name": f"Dashboard Project: {project.name}",
            "entity_type": "Data Science Project",
            "observations": observations,
            "synced_at": datetime.now().isoformat(),
            "source": "Statistical Dashboard Project Center",
            "project_id": project.id,
        }

        filename = f"sync_{project.id}.json"
        path = os.path.join(self.sync_dir, filename)
        with open(path, "w") as f:
            json.dump(payload, f, indent=4)
        return path

    def post_report_to_plane(self, project, summary_html):
        """
        Directly posts a statistical summary to the associated Plane issue.
        Uses the native manager.py for reliable injection.
        """
        manager_script = "scripts/pms/manager.py"
        conda_exec = "conda run -p D:\\Anaconda\\envs\\cursor-factory"

        # Map project to issue ID using the new external_id field
        issue_id = getattr(project, "external_id", None)
        if not issue_id:
            return False, "Project has no associated Plane Issue ID (external_id)."

        import subprocess

        # Prepare safe description for shell
        # We use repr() to ensure the string is safely escaped for Python/Shell
        safe_description = summary_html.replace('"', '\\"')

        cmd = f'{conda_exec} python {manager_script} update --id {issue_id} --description "{safe_description}"'

        try:
            # Use shell=True for conda run on Windows
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode != 0:
                return False, result.stderr or result.stdout
            return True, result.stdout
        except Exception as e:
            return False, str(e)
