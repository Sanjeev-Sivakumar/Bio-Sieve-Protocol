"""Unit tests for Module 1: Fragment Affinity Analyzer."""

import unittest
from fragment_affinity import CharacterStats, FragmentAffinityAnalyzer


class TestFragmentAffinityAnalyzer(unittest.TestCase):
    """Test suite for FragmentAffinityAnalyzer."""

    def setUp(self) -> None:
        self.analyzer = FragmentAffinityAnalyzer(default_strides=[1, 2, 3, 4])

    def test_shannon_entropy_empty(self) -> None:
        """Verify entropy on empty input returns 0.0."""
        raw, norm = self.analyzer.calculate_shannon_entropy("")
        self.assertEqual(raw, 0.0)
        self.assertEqual(norm, 0.0)

    def test_shannon_entropy_single_char(self) -> None:
        """Verify entropy of a repeated single character is 0.0."""
        raw, norm = self.analyzer.calculate_shannon_entropy("AAAAAAA")
        self.assertEqual(raw, 0.0)
        self.assertEqual(norm, 0.0)

    def test_shannon_entropy_uniform_alphabet(self) -> None:
        """Verify entropy of uniform 4-base string is 2.0 bits and normalized 1.0."""
        raw, norm = self.analyzer.calculate_shannon_entropy("ACGTACGTACGTACGT")
        self.assertAlmostEqual(raw, 2.0, places=2)
        self.assertAlmostEqual(norm, 1.0, places=2)

    def test_character_stats(self) -> None:
        """Verify character frequency statistics and compression ratio."""
        stats = self.analyzer.calculate_character_stats("AATTCGG")
        self.assertEqual(stats.total_length, 7)
        self.assertEqual(stats.unique_tokens, 4)
        self.assertEqual(stats.counts["A"], 2)
        self.assertEqual(stats.counts["T"], 2)
        self.assertIn("A", stats.alphabet)
        self.assertTrue(0.0 <= stats.compression_ratio <= 1.0)

    def test_dynamic_affinity_matrix(self) -> None:
        """Verify dynamic matrix dimensions and properties."""
        text = "ATGCATGCATGCATGC"
        labels, matrix = self.analyzer.build_affinity_matrix(text, token_size=2)
        self.assertGreater(len(labels), 0)
        self.assertEqual(len(matrix), len(labels))
        for row in matrix:
            self.assertEqual(len(row), len(labels))
            for val in row:
                self.assertTrue(0.0 <= val <= 1.0)
        # Diagonals must equal 1.0
        for i in range(len(labels)):
            self.assertAlmostEqual(matrix[i][i], 1.0, places=2)

    def test_synthetic_interleave_and_reconstruction(self) -> None:
        """Verify synthetic fragmentation and de-shuffling reconstruction."""
        original = "HELLOWORLD"
        frags = self.analyzer.simulate_fragmentation(original, stride=2)
        self.assertEqual(len(frags), 2)
        reconstructed, conf = self.analyzer.reconstruct_fragments(frags, stride=2)
        self.assertEqual(reconstructed, original)
        self.assertTrue(0.0 <= conf <= 1.0)

    def test_type_error_on_non_string(self) -> None:
        """Verify TypeError is raised if non-string input is provided."""
        with self.assertRaises(TypeError):
            self.analyzer.analyze(12345)  # type: ignore


if __name__ == "__main__":
    unittest.main()
