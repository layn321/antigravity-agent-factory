import json
import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime


class DataGuard:
    """
    Proactive monitoring agent for identifying statistical anomalies in KPIs.
    """

    def __init__(self, config_path):
        with open(config_path, "r") as f:
            self.config = json.load(f)
        self.project_root = Path(config_path).parent.parent

    def detect_zscore_anomaly(self, data, threshold):
        if len(data) < 2:
            return False
        mean = np.mean(data)
        std = np.std(data)
        if std == 0:
            return False
        z_score = abs((data[-1] - mean) / std)
        return z_score > threshold

    def detect_iqr_anomaly(self, data, threshold):
        if len(data) < 4:
            return False
        q1, q3 = np.percentile(data, [25, 75])
        iqr = q3 - q1
        lower_bound = q1 - (threshold * iqr)
        upper_bound = q3 + (threshold * iqr)
        return data[-1] < lower_bound or data[-1] > upper_bound

    def run_checks(self, historical_data):
        """
        Runs checks against historical_data (dict of KPI_ID -> List of values).
        Returns a list of detected anomalies.
        """
        alerts = []
        for kpi_cfg in self.config["monitored_kpis"]:
            kpi_id = kpi_cfg["id"]
            if kpi_id not in historical_data:
                continue

            values = historical_data[kpi_id]
            is_anomaly = False

            if kpi_cfg["method"] == "z-score":
                is_anomaly = self.detect_zscore_anomaly(values, kpi_cfg["threshold"])
            elif kpi_cfg["method"] == "iqr":
                is_anomaly = self.detect_iqr_anomaly(values, kpi_cfg["threshold"])
            elif kpi_cfg["method"] == "static":
                is_anomaly = values[-1] > kpi_cfg.get("max_val", float("inf"))

            if is_anomaly:
                alerts.append(
                    {
                        "kpi_id": kpi_id,
                        "value": values[-1],
                        "method": kpi_cfg["method"],
                        "timestamp": datetime.now().isoformat(),
                    }
                )
        return alerts


if __name__ == "__main__":
    # Example usage / mock run
    config = Path(__file__).parent.parent / "config" / "dataguard_config.json"
    guard = DataGuard(config)

    # Mock some data
    mock_data = {
        "UPH": [100, 102, 98, 105, 101, 40],  # Massive drop
        "DOCK_TO_STOCK": [1.5, 1.8, 2.5],  # Static violation (> 2.0)
    }

    anomalies = guard.run_checks(mock_data)
    print(json.dumps(anomalies, indent=2))
