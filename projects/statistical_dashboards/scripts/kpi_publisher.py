import json
from jinja2 import Template
from pathlib import Path
from datetime import datetime


def publish_dictionary():
    project_root = Path(__file__).parent.parent
    metadata_path = project_root / "docs" / "kpi_metadata.json"
    template_path = project_root / "templates" / "kpi_dictionary.j2"
    output_path = project_root / "docs" / "kpi_dictionary.md"

    if not metadata_path.exists():
        print("Error: Metadata missing. Run scanner first.")
        return

    with open(metadata_path, "r") as f:
        kpis = json.load(f)

    with open(template_path, "r") as f:
        tmpl = Template(f.read())

    output = tmpl.render(kpis=kpis, timestamp=datetime.now().strftime("%Y-%m-%d %H:%M"))

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(output)

    print(f"KPI Dictionary published to {output_path}")


if __name__ == "__main__":
    publish_dictionary()
