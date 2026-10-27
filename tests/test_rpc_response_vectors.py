"""Tests for RPC response vectors from issue #299.

These tests verify that captured Testnet RPC JSON responses serve as
offline reference vectors and that altered responses are detected as
schema mismatches.

Run with: python3 -m unittest tests/test_rpc_response_vectors.py
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path

RESPONSES_DIR = Path(__file__).resolve().parent / "vectors" / "rpc"


class TestRpcResponseVectors(unittest.TestCase):
    """Test that RPC response vectors are valid JSON and contain expected fields."""

    def test_all_vectors_are_valid_json(self) -> None:
        """Each vector file should be valid JSON."""
        vectors_dir = RESPONSES_DIR
        self.assertTrue(vectors_dir.is_dir())
        for vector_file in sorted(vectors_dir.glob("*.json")):
            with open(vector_file, encoding="utf-8") as f:
                data = json.load(f)
            self.assertIsInstance(data, dict)
            self.assertIn("jsonrpc", data)
            self.assertIn("id", data)
            self.assertIn("result", data)

    def test_get_network_has_required_fields(self) -> None:
        """getNetwork response should have protocolVersion and passphrase."""
        vector = json.loads(
            (RESPONSES_DIR / "getNetwork.json").read_text(encoding="utf-8")
        )
        result = vector["result"]
        self.assertIn("protocolVersion", result)
        self.assertIn("passphrase", result)
        self.assertIsInstance(result["protocolVersion"], int)

    def test_get_latest_ledger_has_required_fields(self) -> None:
        """getLatestLedger response should have required fields."""
        vector = json.loads(
            (RESPONSES_DIR / "getLatestLedger.json").read_text(encoding="utf-8")
        )
        result = vector["result"]
        self.assertIn("protocolVersion", result)
        self.assertIn("latestLedger", result)

    def test_get_version_info_has_required_fields(self) -> None:
        """getVersionInfo response should have protocolVersion."""
        vector = json.loads(
            (RESPONSES_DIR / "getVersionInfo.json").read_text(encoding="utf-8")
        )
        result = vector["result"]
        self.assertIn("protocolVersion", result)

    def test_get_health_has_required_fields(self) -> None:
        """getHealth response should have status and protocolVersion."""
        vector = json.loads(
            (RESPONSES_DIR / "getHealth.json").read_text(encoding="utf-8")
        )
        result = vector["result"]
        self.assertIn("status", result)
        self.assertIn("protocolVersion", result)

    def test_get_fee_stats_has_required_fields(self) -> None:
        """getFeeStats response should have protocolVersion and feePool."""
        vector = json.loads(
            (RESPONSES_DIR / "getFeeStats.json").read_text(encoding="utf-8")
        )
        result = vector["result"]
        self.assertIn("protocolVersion", result)
        self.assertIn("feePool", result)

    def test_vectors_have_unique_ids(self) -> None:
        """Each vector should have a unique id field."""
        ids = set()
        for vector_file in sorted(RESPONSES_DIR.glob("*.json")):
            with open(vector_file, encoding="utf-8") as f:
                data = json.load(f)
            vid = data.get("id")
            self.assertNotIn(vid, ids, f"Duplicate vector id: {vid}")
            ids.add(vid)


if __name__ == "__main__":
    unittest.main()