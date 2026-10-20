"""Unit test suite for Bio-Sieve Protocol 5.0 Core Algorithmic Engine."""
import os
import unittest
from collections import Counter
from engine import (
    parse_canonical_fasta,
    build_aho_corasick_automaton,
    search_aho_corasick,
    tokenize_kmers,
    compute_vector_cosine_similarity,
    generate_sat_broadcast_payload,
    homomorphic_blind_delta_merge,
    execute_honeynet_redirection,
    execute_mesh_optical_handshake,
    synchronize_mesh_ledger,
    HAZARDOUS_WATCHLIST,
    REFERENCE_TOXIN_PROFILE,
    AUTOMATON_ROOT
)

class TestBioSieveEngine(unittest.TestCase):
    
    def test_fasta_parsing_valid(self):
        sample = ">Test_Header_001\nATGT TTCC CAA\nggccttaaa"
        res = parse_canonical_fasta(sample)
        self.assertTrue(res["is_valid"])
        self.assertEqual(res["sequence"], "ATGTTTCCCAAGGCCTTAAA")
        self.assertEqual(res["length"], 20)
        self.assertEqual(len(res["sha256"]), 64)
        self.assertEqual(res["header_count"], 1)

    def test_fasta_parsing_empty(self):
        res = parse_canonical_fasta("   \n>header_only\n")
        self.assertFalse(res["is_valid"])
        self.assertEqual(res["length"], 0)
        self.assertIsNotNone(res["error"])

    def test_fasta_parsing_invalid_characters(self):
        sample = ">Header\nZZZZZZZZZZZZZZZZZZZZZZZZ"
        res = parse_canonical_fasta(sample)
        self.assertFalse(res["is_valid"])
        self.assertGreater(res["non_canonical_count"], 0)

    def test_aho_corasick_exact_matches(self):
        seq = "NNNATGTTTCCCAANNNGGCCTTAAANNN"
        matches, elapsed = search_aho_corasick(AUTOMATON_ROOT, seq)
        matched_patterns = [m["pattern"] for m in matches]
        self.assertIn("ATGTTTCCCAA", matched_patterns)
        self.assertIn("GGCCTTAAA", matched_patterns)
        self.assertGreater(elapsed, 0.0)

    def test_aho_corasick_no_match(self):
        seq = "AAAAAAAAAAAAACCCCCCCCCCCCC"
        matches, _ = search_aho_corasick(AUTOMATON_ROOT, seq)
        self.assertEqual(len(matches), 0)

    def test_kmer_tokenization(self):
        seq = "ATGCA"
        kmers, elapsed = tokenize_kmers(seq, k=3)
        self.assertIn("ATG", kmers)
        self.assertIn("TGC", kmers)
        self.assertIn("GCA", kmers)
        self.assertEqual(len(kmers), 3)
        self.assertGreaterEqual(elapsed, 0.0)

    def test_cosine_similarity_identical(self):
        v1 = Counter({"AAA": 2, "CCC": 3, "GGG": 1})
        v2 = Counter({"AAA": 2, "CCC": 3, "GGG": 1})
        sim, elapsed = compute_vector_cosine_similarity(v1, v2)
        self.assertAlmostEqual(sim, 1.0, places=5)
        self.assertGreaterEqual(elapsed, 0.0)

    def test_cosine_similarity_orthogonal(self):
        v1 = Counter({"AAA": 2})
        v2 = Counter({"CCC": 3})
        sim, elapsed = compute_vector_cosine_similarity(v1, v2)
        self.assertEqual(sim, 0.0)

    def test_homomorphic_delta_merge(self):
        base = Counter({"AAA": 1.0, "CCC": 2.0})
        payload = generate_sat_broadcast_payload(1.0)
        merged, telemetry = homomorphic_blind_delta_merge(base, payload)
        self.assertIn("ciphertext_hash", telemetry)
        self.assertIn("poly_degree_N", telemetry)
        self.assertEqual(telemetry["poly_degree_N"], 8192)
        self.assertTrue(len(merged) >= len(base))

    def test_honeynet_redirection(self):
        result = execute_honeynet_redirection(
            seq_hash="1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
            threat_details="Unit_Test_Threat"
        )
        self.assertTrue(os.path.exists(result["filepath"]))
        with open(result["filepath"], "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("; BIO-SIEVE HONEY-NET SILENT REDIRECTION BLUEPRINT", content)
        self.assertIn("INERT SUGAR MATRIX", content)

    def test_mesh_handshake_and_ledger(self):
        sample_nodes = [
            {"node_id": "NODE_ALPHA_SGX", "pcr0_measurement": "0xAA11", "status": "ONLINE"},
            {"node_id": "NODE_BETA_SEV", "pcr0_measurement": "0xBB22", "status": "ONLINE"},
            {"node_id": "NODE_GAMMA_APPLE", "pcr0_measurement": "0xCC33", "status": "ONLINE"},
            {"node_id": "NODE_DELTA_NITRO", "pcr0_measurement": "0xDD44", "status": "ONLINE"}
        ]
        nodes, stats = execute_mesh_optical_handshake(sample_nodes, 1.0)
        self.assertEqual(len(nodes), 4)
        for node in nodes:
            self.assertIn("node_id", node)
            self.assertIn("mesh_latency", node)
            self.assertIn("bandwidth", node)
            self.assertIn("compliance_state", node)
            
        updated = synchronize_mesh_ledger(nodes, 1.1)
        self.assertEqual(len(updated), 4)
        self.assertEqual(updated[0]["synced_db_index"], "v1.1")

    def test_steganographic_fragment_de_shuffler(self):
        from engine import de_shuffle_steganographic_fragments, compute_shannon_entropy
        
        # Craft an interleaved steganographic sequence where pattern GGCCTTAAA is at stride 2
        # G . G . C . C . T . T . A . A . A
        stego_seq = "AGTGCCCTCATAACAAAG"
        res = de_shuffle_steganographic_fragments(stego_seq)
        self.assertIn("entropy", res)
        self.assertGreater(res["entropy"], 0.0)
        self.assertIn("affinity_matrix", res)
        self.assertIn("bonding_affinity_pct", res)
        self.assertIn("thermodynamic_score_kcal_mol", res)

    def test_runtime_execution_matrix_simulator(self):
        from engine import simulate_runtime_execution_matrix
        seq = "ATGCGATCGATCGATCGATCGATCGATC"
        res = simulate_runtime_execution_matrix(seq, is_stego_detected=False, exact_matches_count=0)
        self.assertIn("nozzle_temp_c", res)
        self.assertIn("flow_reynolds_number", res)
        self.assertIn("thermal_gradient_delta_k_um", res)
        self.assertIn("kinetic_rearrangement_prob", res)
        self.assertFalse(res["interlock_triggered"])
        
        # Triggered scenario
        res_trig = simulate_runtime_execution_matrix(seq, is_stego_detected=True, exact_matches_count=1)
        self.assertTrue(res_trig["interlock_triggered"])
        self.assertEqual(res_trig["interlock_relay_state"], "ENGAGED // TRIPPED")

    def test_ephemeral_honeynet_invalidation(self):
        from engine import execute_ephemeral_honeynet_invalidation
        res = execute_ephemeral_honeynet_invalidation(
            seq_hash="abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789",
            isolation_reason="Steganographic Clustered Anomaly"
        )
        self.assertEqual(res["spoofed_status_message"], "[OPERATIONAL STATUS: PIPELINE DISPATCHED TO OUTBOUND SPOOLER]")
        self.assertTrue(os.path.exists(res["filepath"]))
        self.assertGreater(res["enzyme_saturation_pct"], 90.0)
        self.assertIn("TOKEN-QT-", res["isolation_token"])


if __name__ == "__main__":
    unittest.main()
