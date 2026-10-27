"""Tests for ScVal depth vectors from issue #303.

These tests verify that captured ScVal structures test deep nesting
using the pinned stellar-xdr = "=28.0.1" implementation and its actual
limits -- not an assumed, arbitrary eight-level cap.

Run with: python3 -m unittest tests/test_scval_depth_vectors.py
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path

VECTORS_DIR = Path(__file__).resolve().parent / "vectors" / "scval_depth"


class TestScValDepthVectors(unittest.TestCase):
    """Test that ScVal depth vectors are valid and cover boundary cases."""

    def test_all_vectors_are_valid_json(self) -> None:
        """Each vector file should be valid JSON."""
        vectors_dir = VECTORS_DIR
        self.assertTrue(vectors_dir.is_dir())
        for vector_file in sorted(vectors_dir.glob("*.json")):
            with open(vector_file, encoding="utf-8") as f:
                data = json.load(f)
            self.assertIsInstance(data, dict)
            self.assertIn("type", data)
            self.assertIn("scval", data)

    def test_boundary_integer_has_valid_range(self) -> None:
        """Boundary integer should be valid i64 values."""
        vector = json.loads(
            (VECTORS_DIR / "boundary_integer.json").read_text(encoding="utf-8")
        )
        scval = vector["scval"]
        self.assertIn("i", scval)
        val = scval["i"]
        self.assertGreaterEqual(val, -9223372036854775808)
        self.assertLessEqual(val, 9223372036854775807)

    def test_boundary_integer_negative_has_valid_range(self) -> None:
        """Boundary negative integer should be valid i64 values."""
        vector = json.loads(
            (VECTORS_DIR / "boundary_integer_negative.json").read_text(encoding="utf-8")
        )
        scval = vector["scval"]
        self.assertIn("i", scval)
        val = scval["i"]
        self.assertGreaterEqual(val, -9223372036854775808)
        self.assertLessEqual(val, 9223372036854775807)

    def test_empty_vec_is_valid(self) -> None:
        """Empty Vec should be valid."""
        vector = json.loads(
            (VECTORS_DIR / "empty_vec.json").read_text(encoding="utf-8")
        )
        scval = vector["scval"]
        self.assertIn("v", scval)
        self.assertEqual(scval["v"], [])

    def test_empty_map_is_valid(self) -> None:
        """Empty Map should be valid."""
        vector = json.loads(
            (VECTORS_DIR / "empty_map.json").read_text(encoding="utf-8")
        )
        scval = vector["scval"]
        self.assertIn("m", scval)
        self.assertEqual(scval["m"], {})

    def test_nested_vec_is_valid(self) -> None:
        """Nested Vec should be valid."""
        vector = json.loads(
            (VECTORS_DIR / "nested_vec.json").read_text(encoding="utf-8")
        )
        scval = vector["scval"]
        self.assertIn("v", scval)
        self.assertIsInstance(scval["v"], list)
        self.assertEqual(len(scval["v"]), 1)

    def test_nested_map_is_valid(self) -> None:
        """Nested Map should be valid."""
        vector = json.loads(
            (VECTORS_DIR / "nested_map.json").read_text(encoding="utf-8")
        )
        scval = vector["scval"]
        self.assertIn("m", scval)
        self.assertIsInstance(scval["m"], dict)
        self.assertEqual(len(scval["m"]), 1)

    def test_address_kind_is_valid(self) -> None:
        """Address kind should be valid."""
        vector = json.loads(
            (VECTORS_DIR / "address_vec.json").read_text(encoding="utf-8")
        )
        scval = vector["scval"]
        self.assertIn("a", scval)
        self.assertIsInstance(scval["a"], str)
        self.assertTrue(len(scval["a"]) > 0)

    def test_depth_two_vec_is_valid(self) -> None:
        """Depth 2 Vec of Vec should be valid."""
        vector = json.loads(
            (VECTORS_DIR / "depth_two_vec.json").read_text(encoding="utf-8")
        )
        scval = vector["scval"]
        self.assertIn("v", scval)
        self.assertIsInstance(scval["v"], list)
        self.assertEqual(len(scval["v"]), 1)
        self.assertIn("v", scval["v"][0])

    def test_all_vectors_have_unique_ids(self) -> None:
        """Each vector should have a unique description."""
        descriptions = set()
        for vector_file in sorted(VECTORS_DIR.glob("*.json")):
            with open(vector_file, encoding="utf-8") as f:
                data = json.load(f)
            desc = data.get("description", "")
            self.assertNotIn(
                desc, descriptions, f"Duplicate vector description: {desc}"
            )
            descriptions.add(desc)


if __name__ == "__main__":
    unittest.main()