"""Main Pipeline Orchestrator and CLI Runner.

Decentralized Air-Gapped Bio-Sieve Protocol — Offline Simulation & Telemetry Framework.

Executes:
1. Fragment Affinity Analyzer (Module 1)
2. Runtime Physics and Interlock Simulator (Module 2)
3. Ephemeral Validation and Safe Output Engine (Module 3)
4. Monochrome High-Contrast Dashboard Display (Module 4)

Usage:
  python main.py --synthetic-demo
  python main.py --input "ATGCGTACGTTAGCTACGT"
  python main.py --file sample_benign.fasta
  python main.py --file sample_threat.fasta
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional

from dashboard import MonochromeTerminalDashboard
from fragment_affinity import FragmentAffinityAnalyzer
from thermal_interlock import RuntimePhysicsSimulator
from validation_engine import EphemeralValidationEngine, PeerRegistryMesh


class BioSievePipeline:
    """End-to-end coordinator running all 3 offline subsystems deterministically."""

    def __init__(self, output_dir: Optional[str] = None) -> None:
        """Initialize the pipeline with local in-memory registry and physics simulator."""
        self.output_dir = output_dir or "."
        self.analyzer = FragmentAffinityAnalyzer()
        self.physics = RuntimePhysicsSimulator()
        self.registry = PeerRegistryMesh()
        self.validation = EphemeralValidationEngine(
            output_directory=self.output_dir,
            registry=self.registry,
        )
        self.dashboard = MonochromeTerminalDashboard(line_width=86)

    def run_pipeline(self, raw_input: str, print_dashboard: bool = True) -> dict:
        """Execute the end-to-end simulation pipeline on a given input string."""
        # 1. Fragment Affinity Analysis
        affinity_result = self.analyzer.analyze(raw_input)

        # 2. Physics Simulation & Safety Interlock Evaluation
        telemetry = self.physics.simulate(
            input_length=affinity_result.input_length,
            shannon_entropy=affinity_result.stats.shannon_entropy,
            normalized_entropy=affinity_result.stats.normalized_entropy,
        )

        # 3. Ephemeral Validation & Safe Neutralization Spooler
        validation_report = self.validation.validate_and_process(
            raw_input=raw_input,
            affinity_result=affinity_result,
            telemetry=telemetry,
        )

        # 4. Render Monochrome Telemetry Dashboard
        if print_dashboard:
            self.dashboard.print_dashboard(
                raw_input=raw_input,
                affinity_result=affinity_result,
                telemetry=telemetry,
                validation_report=validation_report,
            )

        return {
            "affinity": affinity_result,
            "telemetry": telemetry,
            "validation": validation_report,
        }


def run_synthetic_demonstration(pipeline: BioSievePipeline) -> None:
    """Run 3 representative synthetic test cases showcasing nominal, interleaved, and interlock behaviors."""
    print("\n" + "=" * 86)
    print("RUNNING DEMONSTRATION 1: NOMINAL SYNTHETIC CONTROL SEQUENCE".center(86))
    print("=" * 86 + "\n")
    nominal_seq = "ATGCTAGCATCGTAGCTAGCTAGCTAGCATCGATCGATCGTAGCTAGCTAGCTAGCTA"
    pipeline.run_pipeline(nominal_seq)

    print("\n" + "=" * 86)
    print("RUNNING DEMONSTRATION 2: SYNTHETIC INTERLEAVED FRAGMENTS (DE-SHUFFLER)".center(86))
    print("=" * 86 + "\n")
    # Synthetic interleaved pattern: non-contiguous phased windows
    frag1 = "ATGCATGCATGCATGC"
    frag2 = "CGTACGTACGTACGTA"
    # Interleave at stride 2
    interleaved = "".join(a + b for a, b in zip(frag1, frag2))
    pipeline.run_pipeline(interleaved)

    print("\n" + "=" * 86)
    print("RUNNING DEMONSTRATION 3: HIGH-STRESS SEQUENCE (TRIPS HARDWARE INTERLOCK)".center(86))
    print("=" * 86 + "\n")
    # Long, highly variable string that triggers high Reynolds number and thermal gradient
    high_stress_seq = (
        "ACGT" * 400 + "GATC" * 300 + "TTAG" * 200 + "CCTA" * 150
    )
    pipeline.run_pipeline(high_stress_seq)


def main() -> None:
    """CLI entry point for Bio-Sieve Offline Simulation."""
    parser = argparse.ArgumentParser(
        description="The Decentralized Air-Gapped Bio-Sieve Protocol — Offline Simulation & Telemetry",
    )
    parser.add_argument(
        "--input",
        type=str,
        help="Direct sequence string to analyze",
    )
    parser.add_argument(
        "--file",
        type=str,
        help="Path to a text or FASTA file to read as input",
    )
    parser.add_argument(
        "--synthetic-demo",
        action="store_true",
        help="Run comprehensive 3-case synthetic demonstration",
    )
    parser.add_argument(
        "--reset-interlock",
        action="store_true",
        help="Explicitly reset the session-local hardware interlock",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=".",
        help="Directory to save inert_sugar_blueprint.gcode (default: current directory)",
    )
    parser.add_argument(
        "--html-export",
        type=str,
        default="",
        help="Optional path to export high-contrast monochrome HTML report",
    )

    parser.add_argument(
        "--test-array",
        action="store_true",
        help="Execute automated integration testing array and display telemetry table",
    )

    args = parser.parse_args()

    if args.test_array:
        import run_test_array
        run_test_array.main()
        return

    pipeline = BioSievePipeline(output_dir=args.output_dir)

    if args.reset_interlock:
        pipeline.physics.reset_interlock()
        print("[Bio-Sieve Engine]: Session hardware interlock has been reset to ARMED.")
        return

    if args.synthetic_demo:
        run_synthetic_demonstration(pipeline)
        return

    raw_input = ""
    if args.input:
        raw_input = args.input.strip()
    elif args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"[Error]: File not found: {args.file}", file=sys.stderr)
            sys.exit(1)
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        # Strip FASTA header lines starting with '>'
        raw_input = "".join(line.strip() for line in lines if not line.startswith(">"))
    else:
        # Default fallback to synthetic demo if no argument passed
        print("[Notice]: No input provided. Launching standard synthetic demonstration suite...\n")
        run_synthetic_demonstration(pipeline)
        return

    if not raw_input:
        print("[Error]: Input sequence is empty.", file=sys.stderr)
        sys.exit(1)

    result = pipeline.run_pipeline(raw_input)

    if args.html_export:
        html = pipeline.dashboard.render_monochrome_html(
            raw_input=raw_input,
            affinity_result=result["affinity"],
            telemetry=result["telemetry"],
            validation_report=result["validation"],
        )
        with open(args.html_export, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"\n[Bio-Sieve Engine]: Monochrome HTML report written to: {args.html_export}")


if __name__ == "__main__":
    main()
