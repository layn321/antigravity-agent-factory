import json
from jinja2 import Template
from pathlib import Path
from datetime import datetime
import uuid


class ReportGenerator:
    """
    Synthesizes dashboard data into professional stakeholder reports.
    """

    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.template_path = self.project_root / "templates" / "exec_summary.j2"
        self.output_dir = self.project_root / "reports"

    def load_metadata(self):
        meta_path = self.project_root / "docs" / "kpi_metadata.json"
        if meta_path.exists():
            with open(meta_path, "r") as f:
                return json.load(f)
        return []

    def generate_summary(self, mock_kpi_values, mock_alerts=None):
        kpi_meta = self.load_metadata()
        summary_data = []

        # Map metadata to current values
        for meta in kpi_meta:
            kid = meta["id"]
            val = mock_kpi_values.get(kid, "N/A")

            # Simple status logic for mock
            status = "✅"
            insight = "Performing within normal parameters."
            if kid == "UPH" and val < 50:
                status = "🔴"
                insight = "Significant productivity drop detected."
            if kid == "DOCK_TO_STOCK" and val > 2.0:
                status = "🟡"
                insight = "Approaching critical threshold."

            summary_data.append(
                {
                    "name": meta["name"],
                    "value": val,
                    "unit": meta["unit"],
                    "status_icon": status,
                    "insight": insight,
                }
            )

        with open(self.template_path, "r") as f:
            tmpl = Template(f.read())

        report_id = str(uuid.uuid4())[:8].upper()
        now = datetime.now()

        output = tmpl.render(
            timestamp=now.strftime("%Y-%m-%d %H:%M"),
            kpi_summary=summary_data,
            alerts=mock_alerts or [],
            report_id=report_id,
        )

        filename = f"exec_summary_{now.strftime('%Y%m%d_%H%M')}.md"
        report_path = self.output_dir / filename
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(output)

        return report_path


if __name__ == "__main__":
    root = Path(__file__).parent.parent
    gen = ReportGenerator(root)

    # Mock data injection
    current_values = {
        "INV_TURNOVER": 12.5,
        "BIN_DENSITY": 88.2,
        "DOCK_TO_STOCK": 2.15,
        "UPH": 42.0,
    }
    mock_alerts = [
        {"kpi_id": "UPH", "method": "z-score", "value": 42.0},
        {"kpi_id": "DOCK_TO_STOCK", "method": "static", "value": 2.15},
    ]

    path = gen.generate_summary(current_values, mock_alerts)
    print(f"Executive Summary generated at: {path}")
