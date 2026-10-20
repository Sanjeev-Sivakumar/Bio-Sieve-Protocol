"""Fragment Affinity Analyzer Module (Module 1).

Decentralized Air-Gapped Bio-Sieve Protocol — Offline Simulation & Telemetry Framework.

Features:
- Non-contiguous character window scanning with configurable offsets and strides.
- Dynamic Shannon entropy calculation, character frequency statistics, and Lempel-Ziv complexity.
- Dynamically sized token affinity matrix computed 100% at runtime from input properties.
- Normalized affinity scoring and fragment reconstruction confidence metric.
- Safe synthetic fragment grouping and de-shuffling demonstration.
- Pure Python standard library implementation with zero external network or model dependencies.
"""

from __future__ import annotations

import math
import time
from collections import Counter
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


@dataclass(frozen=True)
class CharacterStats:
    """Character-level frequency and complexity statistics."""
    total_length: int
    unique_tokens: int
    alphabet: List[str]
    frequencies: Dict[str, float]
    counts: Dict[str, int]
    shannon_entropy: float
    normalized_entropy: float
    compression_ratio: float


@dataclass
class AffinityAnalysisResult:
    """Complete results from the fragment affinity analyzer."""
    input_length: int
    stats: CharacterStats
    strides_analyzed: List[int]
    token_labels: List[str]
    matrix_dimensions: Tuple[int, int]
    affinity_matrix: List[List[float]]
    mean_affinity_score: float
    max_affinity_score: float
    reconstruction_confidence: float
    reconstructed_string: str
    is_fragmentation_detected: bool
    execution_time_ms: float
    metadata: Dict[str, Any] = field(default_factory=dict)


class FragmentAffinityAnalyzer:
    """Analyzes character strings across non-contiguous windows and computes dynamic affinities.

    All metrics are computed deterministically at runtime from the provided input string.
    """

    def __init__(self, default_strides: Optional[List[int]] = None) -> None:
        """Initialize the analyzer with configurable strides.

        Args:
            default_strides: List of non-contiguous stride offsets to inspect.
                             Defaults to [1, 2, 3, 4, 5].
        """
        self.strides: List[int] = default_strides if default_strides is not None else [1, 2, 3, 4, 5]

    @staticmethod
    def calculate_shannon_entropy(text: str) -> Tuple[float, float]:
        """Compute the Shannon entropy and normalized entropy for a given text string.

        Formula:
            H(X) = - sum(p(x) * log2(p(x)))
            H_norm = H(X) / log2(max(2, |alphabet|))

        Args:
            text: Input string to evaluate.

        Returns:
            Tuple of (raw Shannon entropy in bits, normalized entropy in [0.0, 1.0]).
        """
        if not text:
            return 0.0, 0.0

        length = len(text)
        counts = Counter(text)
        entropy = 0.0

        for count in counts.values():
            p = count / length
            if p > 0.0:
                entropy -= p * math.log2(p)

        alphabet_size = len(counts)
        max_possible_entropy = math.log2(max(2, alphabet_size))
        normalized = min(1.0, max(0.0, entropy / max_possible_entropy)) if max_possible_entropy > 0 else 0.0
        return round(entropy, 4), round(normalized, 4)

    @classmethod
    def calculate_character_stats(cls, text: str) -> CharacterStats:
        """Derive comprehensive character distribution and algorithmic complexity metrics.

        Args:
            text: Input string.

        Returns:
            CharacterStats dataclass containing counts, frequencies, and entropy.
        """
        length = len(text)
        if length == 0:
            return CharacterStats(
                total_length=0,
                unique_tokens=0,
                alphabet=[],
                frequencies={},
                counts={},
                shannon_entropy=0.0,
                normalized_entropy=0.0,
                compression_ratio=0.0,
            )

        counts = dict(Counter(text))
        alphabet = sorted(list(counts.keys()))
        frequencies = {char: round(cnt / length, 5) for char, cnt in counts.items()}
        raw_ent, norm_ent = cls.calculate_shannon_entropy(text)

        # Approximate Lempel-Ziv complexity / dictionary compressibility
        lz_seen = set()
        current_sub = ""
        for char in text:
            current_sub += char
            if current_sub not in lz_seen:
                lz_seen.add(current_sub)
                current_sub = ""
        lz_complexity = len(lz_seen)
        theoretical_bound = length / math.log2(max(2, length)) if length > 1 else 1.0
        compression_ratio = round(min(1.0, lz_complexity / theoretical_bound), 4)

        return CharacterStats(
            total_length=length,
            unique_tokens=len(alphabet),
            alphabet=alphabet,
            frequencies=frequencies,
            counts=counts,
            shannon_entropy=raw_ent,
            normalized_entropy=norm_ent,
            compression_ratio=compression_ratio,
        )

    def extract_stride_subsequences(self, text: str, stride: int) -> List[str]:
        """Extract all non-contiguous phased subsequences for a specified stride.

        Args:
            text: Input string.
            stride: Step size for non-contiguous windowing (e.g. 2, 3, 4).

        Returns:
            List of non-contiguous substrings.
        """
        if stride <= 0 or not text:
            return [text] if text else []
        return [text[offset::stride] for offset in range(min(stride, len(text)))]

    def build_affinity_matrix(self, text: str, token_size: int = 2) -> Tuple[List[str], List[List[float]]]:
        """Build a dynamically sized token affinity matrix based on co-occurrence and transition.

        Args:
            text: Input string.
            token_size: Token length for forming the matrix alphabet (k-mer size).

        Returns:
            Tuple of (token labels, square 2D matrix of affinity values in [0.0, 1.0]).
        """
        if len(text) < token_size:
            tokens = [c for c in text] if text else ["?"]
            labels = sorted(list(set(tokens)))
            dim = len(labels)
            return labels, [[1.0 if i == j else 0.0 for j in range(dim)] for i in range(dim)]

        # Extract tokens
        tokens = [text[i:i + token_size] for i in range(len(text) - token_size + 1)]
        counts = Counter(tokens)
        # Select top unique tokens dynamically (up to 16 for readable telemetry matrix)
        top_tokens = [tok for tok, _ in counts.most_common(16)]
        top_tokens.sort()
        dim = len(top_tokens)
        token_index = {tok: idx for idx, tok in enumerate(top_tokens)}

        # Initialize dynamic matrix
        matrix = [[0.0 for _ in range(dim)] for _ in range(dim)]
        co_counts = [[0 for _ in range(dim)] for _ in range(dim)]

        # Scan pairs within local non-contiguous window offsets [1, 2, 3]
        for i in range(len(tokens) - 1):
            tok_a = tokens[i]
            if tok_a not in token_index:
                continue
            idx_a = token_index[tok_a]

            for offset in (1, 2, 3):
                if i + offset < len(tokens):
                    tok_b = tokens[i + offset]
                    if tok_b in token_index:
                        idx_b = token_index[tok_b]
                        co_counts[idx_a][idx_b] += 1
                        co_counts[idx_b][idx_a] += 1

        # Normalize into affinity coefficients in [0.0, 1.0]
        for i in range(dim):
            tok_a = top_tokens[i]
            cnt_a = counts[tok_a]
            for j in range(dim):
                if i == j:
                    matrix[i][j] = 1.0
                else:
                    tok_b = top_tokens[j]
                    cnt_b = counts[tok_b]
                    denom = math.sqrt(cnt_a * cnt_b) * 3.0
                    affinity = co_counts[i][j] / denom if denom > 0 else 0.0
                    matrix[i][j] = round(min(1.0, affinity), 4)

        return top_tokens, matrix

    def simulate_fragmentation(self, text: str, stride: int = 2) -> List[str]:
        """Synthetic helper: simulate non-contiguous interleaved fragmentation of a test string.

        Args:
            text: Test string to interleave.
            stride: Stride interval (e.g. 2 for even/odd splitting).

        Returns:
            List of interleaved fragments.
        """
        if stride < 1 or not text:
            return [text]
        return [text[offset::stride] for offset in range(stride)]

    def reconstruct_fragments(self, fragments: List[str], stride: int = 2) -> Tuple[str, float]:
        """De-shuffle and reassemble interleaved non-contiguous test fragments.

        Args:
            fragments: List of non-contiguous fragments.
            stride: Interleaving stride.

        Returns:
            Tuple of (reconstructed string, confidence score in [0.0, 1.0]).
        """
        if not fragments:
            return "", 0.0
        if len(fragments) == 1:
            return fragments[0], 1.0

        max_len = max(len(f) for f in fragments)
        reconstructed_chars: List[str] = []

        for char_idx in range(max_len):
            for frag in fragments:
                if char_idx < len(frag):
                    reconstructed_chars.append(frag[char_idx])

        reconstructed = "".join(reconstructed_chars)

        # Calculate reconstruction confidence based on fragment length parity and continuity
        lens = [len(f) for f in fragments]
        max_diff = max(lens) - min(lens)
        parity_penalty = min(0.4, (max_diff / (max(lens) + 1)) * 0.5)
        raw_ent, norm_ent = self.calculate_shannon_entropy(reconstructed)
        entropy_factor = 0.85 + (0.15 * norm_ent)
        confidence = round(max(0.1, min(1.0, (1.0 - parity_penalty) * entropy_factor)), 4)

        return reconstructed, confidence

    def analyze(self, text: str, token_size: int = 2) -> AffinityAnalysisResult:
        """Run full affinity analysis, matrix generation, and de-shuffling metrics.

        Args:
            text: Input string to process.
            token_size: Token k-mer size for affinity matrix.

        Returns:
            AffinityAnalysisResult containing complete runtime calculations.
        """
        start_time = time.perf_counter()

        if not isinstance(text, str):
            raise TypeError(f"Input must be a string, got {type(text).__name__}")

        stats = self.calculate_character_stats(text)
        token_labels, matrix = self.build_affinity_matrix(text, token_size=token_size)

        # Compute average and maximum off-diagonal affinity
        dim = len(token_labels)
        off_diagonals: List[float] = []
        for i in range(dim):
            for j in range(dim):
                if i != j:
                    off_diagonals.append(matrix[i][j])

        mean_affinity = round(sum(off_diagonals) / len(off_diagonals), 4) if off_diagonals else 0.0
        max_affinity = round(max(off_diagonals), 4) if off_diagonals else 0.0

        # Evaluate potential non-contiguous fragmentation across configured strides
        is_fragmented = False
        reconstructed = text
        best_confidence = 1.0

        if len(text) >= 24:
            # Check if text shows high periodicity or interleaved patterns
            for stride in self.strides:
                if stride > 1:
                    subseqs = self.extract_stride_subsequences(text, stride)
                    # Require each sub-sequence to have at least 8 characters to avoid small-sample variance
                    if len(subseqs) == stride and all(len(s) >= 8 for s in subseqs):
                        entropies = [self.calculate_shannon_entropy(s)[0] for s in subseqs if s]
                        # Look for significant structural phase difference
                        if entropies and (max(entropies) - min(entropies)) > 0.85:
                            is_fragmented = True
                            reconstructed, best_confidence = self.reconstruct_fragments(subseqs, stride)
                            break

        elapsed_ms = round((time.perf_counter() - start_time) * 1000.0, 3)

        return AffinityAnalysisResult(
            input_length=len(text),
            stats=stats,
            strides_analyzed=list(self.strides),
            token_labels=token_labels,
            matrix_dimensions=(dim, dim),
            affinity_matrix=matrix,
            mean_affinity_score=mean_affinity,
            max_affinity_score=max_affinity,
            reconstruction_confidence=best_confidence,
            reconstructed_string=reconstructed,
            is_fragmentation_detected=is_fragmented,
            execution_time_ms=elapsed_ms,
            metadata={
                "shannon_entropy_bits": stats.shannon_entropy,
                "normalized_entropy": stats.normalized_entropy,
                "compression_ratio": stats.compression_ratio,
                "unique_tokens": stats.unique_tokens,
            },
        )
