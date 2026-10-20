"""Unit tests for Module 3: Ephemeral Validation and Safe Output Engine."""

import os
import tempfile
import unittest
from fragment_affinity import FragmentAffinityAnalyzer
from thermal_interlock import RuntimePhysicsSimulator, SafetyThresholds
from validation_engine import (
    EphemeralValidationEngine,
    InvertiblePlaceholderGenerator,
    PeerRegistryMesh,
)


class TestEphemeralValidationEngine(unittest.TestCase):
    """Test suite for EphemeralValidationEngine."""

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.registry = PeerRegistryMesh()
        self.engine = EphemeralValidationEngine(
            output_directory=self.temp_dir.name,
            registry=self.registry,
        )
        self.analyzer = FragmentAffinityAnalyzer()
        self.physics = RuntimePhysicsSimulator()

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_nominal_validation_flow(self) -> None:
        """Verify nominal input passes validation and logs to mesh."""
        seq = "ATGCGTACGTTAGCTACGT"
        aff = self.analyzer.analyze(seq)
        telem = self.physics.simulate(len(seq), aff.stats.shannon_entropy, aff.stats.normalized_entropy)

        report = self.engine.validate_and_process(seq, aff, telem)
        self.assertTrue(report.is_validated)
        self.assertEqual(report.validation_verdict, "VALIDATION_PASSED")
        self.assertIn("STANDARD SPOOLER DISPATCHED", report.spooler_status)
        self.assertTrue(report.isolation_id.startswith("TOKEN-ISO-"))
        self.assertEqual(self.registry.count(), 1)

        # Check G-code exists and is safe
        self.assertTrue(os.path.exists(report.gcode_file_path))
        with open(report.gcode_file_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("M104 S0", content)  # Heater OFF
        self.assertIn("G90", content)
        self.assertIn("G21", content)
        self.assertIn(report.isolation_id, content)

    def test_safety_failure_reporting(self) -> None:
        """Verify safety failure triggers transparent failure reason and requires validation."""
        seq = "ATGC"
        aff = self.analyzer.analyze(seq)
        # Create tripped physics simulator
        strict_physics = RuntimePhysicsSimulator(thresholds=SafetyThresholds(max_core_temp_c=10.0))
        telem = strict_physics.simulate(len(seq), 2.0, 1.0)

        report = self.engine.validate_and_process(seq, aff, telem)
        self.assertFalse(report.is_validated)
        self.assertEqual(report.validation_verdict, "VALIDATION_FAILED")
        self.assertIn("OUTPUT VALIDATION REQUIRED", report.spooler_status)
        self.assertGreater(len(report.failed_checks), 0)
        self.assertTrue(any("INTERLOCK_STATE_TRIPPED" in chk for chk in report.failed_checks))


if __name__ == "__main__":
    unittest.main()
