import os
import re
import yaml
import json
from pathlib import Path


class KPIScanner:
    """
    Scans files for @KPI annotations and aggregates them into metadata.
    """

    def __init__(self, root_dir):
        self.root_dir = Path(root_dir)
        self.kpi_pattern = re.compile(
            r'@KPI:\s*\n(.*?)(?=\n\s*"""|\n\s*@|$)', re.DOTALL
        )

    def scan_files(self):
        kpis = []
        # Focus on core logic and SQL folders
        search_dirs = [self.root_dir / "core", self.root_dir / "schemas"]

        for sdir in search_dirs:
            if not sdir.exists():
                continue
            for path in sdir.rglob("*"):
                if path.suffix in [".py", ".sql"]:
                    content = path.read_text(encoding="utf-8", errors="ignore")
                    matches = self.kpi_pattern.finditer(content)
                    for match in matches:
                        try:
                            kpi_data = yaml.safe_load(match.group(1))
                            if kpi_data:
                                kpi_data["source_file"] = str(
                                    path.relative_to(self.root_dir)
                                )
                                kpis.append(kpi_data)
                        except yaml.YAMLError as e:
                            print(f"Error parsing KPI in {path}: {e}")
        return kpis

    def save_metadata(self, kpis, output_path):
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(kpis, f, indent=2)


if __name__ == "__main__":
    project_root = Path(__file__).parent.parent
    scanner = KPIScanner(project_root)
    results = scanner.scan_files()
    output = project_root / "docs" / "kpi_metadata.json"
    scanner.save_metadata(results, output)
    print(f"Successfully extracted {len(results)} KPIs to {output}")
