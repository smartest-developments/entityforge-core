"""Sanity checks for the offline dashboard bundle."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


class DashboardBundleTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.mvp_root = Path(__file__).resolve().parents[1]
        cls.dashboard_dir = cls.mvp_root / "dashboard"

    def test_required_files_exist(self) -> None:
        required = [
            "index.html",
            "management_dashboard.html",
            "management_dashboard.css",
            "management_dashboard.js",
            "management_dashboard_data.js",
            "tabler.min.css",
            "tabler.min.js",
            "chart.umd.js",
        ]
        missing = [name for name in required if not (self.dashboard_dir / name).exists()]
        self.assertFalse(missing, msg=f"Missing dashboard files: {missing}")

    def test_dashboard_data_payload_is_available(self) -> None:
        data_js = (self.dashboard_dir / "management_dashboard_data.js").read_text(encoding="utf-8")
        match = re.search(r"window\.MVP_DASHBOARD_DATA\s*=\s*(\{.*\})\s*;\s*$", data_js, flags=re.S)
        self.assertIsNotNone(match, "management_dashboard_data.js does not expose window.MVP_DASHBOARD_DATA")
        payload = json.loads(match.group(1))
        self.assertIsInstance(payload, dict)
        self.assertIn("runs", payload)
        self.assertIsInstance(payload.get("runs"), list)
        self.assertGreater(len(payload.get("runs", [])), 0, "Dashboard data has no runs")


if __name__ == "__main__":
    unittest.main(verbosity=2)
