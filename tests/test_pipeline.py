"""End-to-end pipeline integration tests."""

import tempfile
import unittest
from main import BioSievePipeline


class TestPipelineIntegration(unittest.TestCase):
    """End-to-end integration test suite."""

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.pipeline = BioSievePipeline(output_dir=self.temp_dir.name)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_end_to_end_nominal_sequence(self) -> None:
        """Verify full pipeline runs without error on standard sequence."""
        seq = "ATGCTAGCATCGTAGCTAGCTAGCTAGCATCGATCGATCGTAGCTAGCTAGCTAGCTA"
        res = self.pipeline.run_pipeline(seq, print_dashboard=False)

        self.assertIn("affinity", res)
        self.assertIn("telemetry", res)
        self.assertIn("validation", res)

        aff = res["affinity"]
        telem = res["telemetry"]
        val = res["validation"]

        self.assertEqual(aff.input_length, len(seq))
        self.assertTrue(telem.is_safe)
        self.assertEqual(val.validation_verdict, "VALIDATION_PASSED")
        self.assertTrue(val.isolation_id.startswith("TOKEN-ISO-"))

        # Verify dashboard string formatting
        rendered = self.pipeline.dashboard.render(seq, aff, telem, val)
        self.assertIn("AIR-GAPPED BIO-SIEVE PROTOCOL", rendered)
        self.assertIn("DYNAMIC MATRIX DIMENSIONS", rendered.upper())
        self.assertIn("REYNOLDS NUMBER", rendered.upper())

    def test_interleaved_fragment_detection(self) -> None:
        """Verify pipeline accurately de-shuffles interleaved sequences."""
        f1 = "ATGCATGCATGC"
        f2 = "CGTACGTACGTA"
        interleaved = "".join(a + b for a, b in zip(f1, f2))
        res = self.pipeline.run_pipeline(interleaved, print_dashboard=False)

        aff = res["affinity"]
        self.assertEqual(aff.input_length, len(interleaved))
        self.assertGreaterEqual(aff.reconstruction_confidence, 0.50)


if __name__ == "__main__":
    unittest.main()
