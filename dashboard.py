"""High-Contrast Monochrome Dashboard Module.

Decentralized Air-Gapped Bio-Sieve Protocol — Offline Simulation & Telemetry Framework.

Design Principles:
- Strict Monochrome High-Contrast Presentation:
  - Solid black text (#000000) on clean white background (#FFFFFF) or terminal inverse.
  - Zero colored accents (no red, green, yellow, or blue ANSI color sequences).
  - Clean, precise box-drawing table layouts and monospace telemetry feeds.
- 100% Dynamic Telemetry Display:
  - Input length, Shannon entropy, unique character distribution.
  - Affinity matrix dimensions and sample affinity values.
  - Flow Reynolds number, Core Thermal Gradient, Core Temperature.
  - Rearrangement probability, session-local interlock state.
  - Safe output spooler validation status and audit isolation token.
  - Subsystem execution timing in milliseconds.
- Standard Library Only: No external dependencies.
"""

from __future__ import annotations

import sys
from typing import Any, Dict, List, Optional, Tuple

from fragment_affinity import AffinityAnalysisResult
from thermal_interlock import InterlockState, ThermalInterlockTelemetry
from validation_engine import ValidationReport


class MonochromeTerminalDashboard:
    """Renders high-contrast monochrome terminal telemetry dashboards using standard library."""

    def __init__(self, use_ansi_inverse: bool = False, line_width: int = 86, ascii_mode: bool = False) -> None:
        """Initialize dashboard renderer.

        Args:
            use_ansi_inverse: If True, uses ANSI reverse video (\033[7m) for title blocks.
                              Strictly uses zero color accents.
            line_width: Width in characters for table frames.
            ascii_mode: If True, uses standard ASCII characters (+, -, |) for universal terminal compatibility.
        """
        self.use_ansi_inverse = use_ansi_inverse
        self.line_width = line_width
        # Automatically detect if terminal can encode unicode
        if ascii_mode:
            self.ascii_mode = True
        else:
            encoding = getattr(sys.stdout, "encoding", "utf-8") or "utf-8"
            self.ascii_mode = "cp1252" in encoding.lower() or "ascii" in encoding.lower()

    def _frame_line(self, text: str = "", fill: str = " ", left: Optional[str] = None, right: Optional[str] = None) -> str:
        """Helper to create a padded frame line within border characters."""
        l_char = left if left is not None else ("|" if self.ascii_mode else "│")
        r_char = right if right is not None else ("|" if self.ascii_mode else "│")
        inner_width = self.line_width - len(l_char) - len(r_char)
        padded = f" {text}".ljust(inner_width, fill)[:inner_width]
        return f"{l_char}{padded}{r_char}"

    def _center_line(self, text: str = "", left: Optional[str] = None, right: Optional[str] = None) -> str:
        """Helper to center text within borders."""
        l_char = left if left is not None else ("|" if self.ascii_mode else "│")
        r_char = right if right is not None else ("|" if self.ascii_mode else "│")
        inner_width = self.line_width - len(l_char) - len(r_char)
        centered = text.center(inner_width)
        return f"{l_char}{centered}{r_char}"

    def render(
        self,
        raw_input: str,
        affinity_result: AffinityAnalysisResult,
        telemetry: ThermalInterlockTelemetry,
        validation_report: ValidationReport,
    ) -> str:
        """Render complete monochrome telemetry view as a formatted multi-line string.

        All rendered metrics are dynamic runtime values from the pipeline.
        """
        w = self.line_width
        if self.ascii_mode:
            top_border = "+" + "-" * (w - 2) + "+"
            mid_border = "+" + "-" * (w - 2) + "+"
            double_border = "+" + "=" * (w - 2) + "+"
            bot_border = "+" + "-" * (w - 2) + "+"
            unit_deg = " deg C"
            delta_sym = "(Delta_T)"
        else:
            top_border = "┌" + "─" * (w - 2) + "┐"
            mid_border = "├" + "─" * (w - 2) + "┤"
            double_border = "╞" + "═" * (w - 2) + "╡"
            bot_border = "└" + "─" * (w - 2) + "┘"
            unit_deg = " °C"
            delta_sym = "(ΔT)"

        lines: List[str] = []

        # 1. Header Section
        lines.append(top_border)
        lines.append(self._center_line("THE DECENTRALIZED AIR-GAPPED BIO-SIEVE PROTOCOL"))
        lines.append(self._center_line("OFFLINE SIMULATION & DYNAMIC TELEMETRY FRAMEWORK"))
        lines.append(self._center_line("OPERATIONAL SPECIFICATION: AIR-GAPPED // LOCAL IN-MEMORY ONLY"))
        lines.append(double_border)

        # 2. Input Metrics Section
        lines.append(self._frame_line("1. INPUT SEQUENCE TELEMETRY & COMPLEXITY PROFILE"))
        lines.append(mid_border)
        input_preview = raw_input[:40] + ("..." if len(raw_input) > 40 else "")
        lines.append(self._frame_line(f"Sequence Input (Preview)   : {input_preview}"))
        lines.append(self._frame_line(f"Input Character Length     : {affinity_result.input_length} chars"))
        lines.append(self._frame_line(f"Shannon Entropy (H)        : {affinity_result.stats.shannon_entropy:.4f} bits/symbol"))
        lines.append(self._frame_line(f"Normalized Entropy (H_norm): {affinity_result.stats.normalized_entropy:.4f} [0.0 - 1.0]"))
        lines.append(self._frame_line(f"Lempel-Ziv Complexity Ratio: {affinity_result.stats.compression_ratio:.4f}"))
        lines.append(self._frame_line(f"Alphabet Size (|Sigma|)    : {affinity_result.stats.unique_tokens} unique characters"))
        
        # Format top 6 character frequencies
        freq_str = ", ".join(f"'{k}': {v:.1%}" for k, v in list(affinity_result.stats.frequencies.items())[:6])
        lines.append(self._frame_line(f"Character Frequencies      : {freq_str}"))

        # 3. Fragment Affinity Matrix Section
        lines.append(double_border)
        lines.append(self._frame_line("2. FRAGMENT AFFINITY ANALYZER (COMPUTATIONAL AFFINITY ENGINE)"))
        lines.append(mid_border)
        dim_x, dim_y = affinity_result.matrix_dimensions
        lines.append(self._frame_line(f"Dynamic Matrix Dimensions  : {dim_x} x {dim_y} (Dynamically derived at runtime)"))
        lines.append(self._frame_line(f"Strides Evaluated          : {affinity_result.strides_analyzed}"))
        lines.append(self._frame_line(f"Mean Token Affinity Score  : {affinity_result.mean_affinity_score * 100.0:.2f}%"))
        lines.append(self._frame_line(f"Peak Off-Diagonal Affinity : {affinity_result.max_affinity_score * 100.0:.2f}%"))
        lines.append(self._frame_line(f"De-shuffle Confidence      : {affinity_result.reconstruction_confidence * 100.0:.2f}%"))
        lines.append(self._frame_line(f"Fragmentation Detected     : {'YES (NON-CONTIGUOUS PHASED)' if affinity_result.is_fragmentation_detected else 'NO (CONTIGUOUS)'}"))

        # Compact sample affinity matrix display (top 5x5)
        sample_dim = min(dim_x, 5)
        if sample_dim > 0:
            header_tokens = " ".join(f"{lbl:>5}" for lbl in affinity_result.token_labels[:sample_dim])
            lines.append(self._frame_line(f"Matrix Slice (Top {sample_dim}x{sample_dim})    : [TOKENS] {header_tokens}"))
            for r_idx in range(sample_dim):
                row_lbl = affinity_result.token_labels[r_idx]
                row_vals = " ".join(f"{affinity_result.affinity_matrix[r_idx][c_idx]:5.2f}" for c_idx in range(sample_dim))
                lines.append(self._frame_line(f"   Row '{row_lbl}': {row_vals}"))

        # 4. Runtime Physics Telemetry Section
        lines.append(double_border)
        lines.append(self._frame_line("3. RUNTIME EXECUTION MATRIX (PHYSICS-AI TELEMETRY)"))
        lines.append(mid_border)
        lines.append(self._frame_line(f"Core Microchannel Temp     : {telemetry.core_temp_c:.2f}{unit_deg} ({telemetry.core_temp_k:.2f} K)"))
        lines.append(self._frame_line(f"Core Thermal Gradient {delta_sym}: {telemetry.thermal_gradient_k_um:.4f} K/micrometer (Limit: 0.8500)"))
        lines.append(self._frame_line(f"Flow Velocity (v)          : {telemetry.flow_velocity_m_s:.4f} m/s"))
        lines.append(self._frame_line(f"Flow Reynolds Number (Re)  : {telemetry.reynolds_number:.2f} (Regime: {telemetry.flow_regime.value})"))
        lines.append(self._frame_line(f"Microchannel Pressure Drop : {telemetry.pressure_drop_kpa:.3f} kPa (Total: {telemetry.total_pressure_kpa:.3f} kPa)"))
        lines.append(self._frame_line(f"Kinetic Rearrangement Prob : {telemetry.rearrangement_probability:.4f} ({telemetry.rearrangement_probability * 100.0:.2f}%)"))
        
        interlock_status_text = (
            "TRIPPED (SAFETY THRESHOLD BREACHED)"
            if telemetry.interlock_state == InterlockState.TRIPPED
            else "ARMED (ALL THRESHOLDS NOMINAL)"
        )
        lines.append(self._frame_line(f"Hardware Interlock Relay   : {interlock_status_text}"))

        if telemetry.trigger_records:
            lines.append(self._frame_line("  Trigger Measurements:"))
            for tr in telemetry.trigger_records:
                lines.append(self._frame_line(f"    * {tr.parameter_name}: {tr.observed_value} {tr.unit} [Threshold: {tr.threshold_value}]"))

        # 5. Ephemeral Validation & Safe Output Section
        lines.append(double_border)
        lines.append(self._frame_line("4. EPHEMERAL VALIDATION & ACTIVE NEUTRALIZATION ENGINE"))
        lines.append(mid_border)
        lines.append(self._frame_line(f"Validation Verdict         : {validation_report.validation_verdict}"))
        lines.append(self._frame_line(f"Simulated Spooler Status   : [{validation_report.spooler_status}]"))
        lines.append(self._frame_line(f"Security Isolation Token   : {validation_report.isolation_id}"))
        lines.append(self._frame_line(f"Decoy Placeholder File     : {validation_report.gcode_file_path}"))
        lines.append(self._frame_line(f"Decoy File Size            : {validation_report.audit_record.gcode_size_bytes} bytes (Safe sucrose lattice)"))
        lines.append(self._frame_line(f"In-Memory Mesh Audits Logged: {validation_report.in_memory_mesh_count} records"))

        if validation_report.failed_checks:
            lines.append(self._frame_line("  Safety Failure Reasons (Exposed Transparently):"))
            for chk in validation_report.failed_checks:
                lines.append(self._frame_line(f"    * {chk}"))

        # 6. Performance & Execution Timing
        lines.append(double_border)
        total_time = (
            affinity_result.execution_time_ms
            + telemetry.execution_time_ms
            + validation_report.execution_time_ms
        )
        lines.append(self._frame_line(
            f"Timing: Affinity: {affinity_result.execution_time_ms:.2f}ms | "
            f"Physics: {telemetry.execution_time_ms:.2f}ms | "
            f"Validation: {validation_report.execution_time_ms:.2f}ms | "
            f"Total: {total_time:.2f}ms"
        ))
        lines.append(self._frame_line("Architecture: Air-Gapped Local-First. Zero External Network Requests."))
        lines.append(bot_border)

        return "\n".join(lines)

    def print_dashboard(
        self,
        raw_input: str,
        affinity_result: AffinityAnalysisResult,
        telemetry: ThermalInterlockTelemetry,
        validation_report: ValidationReport,
    ) -> None:
        """Print the rendered dashboard directly to standard output with automatic fallback."""
        try:
            rendered = self.render(raw_input, affinity_result, telemetry, validation_report)
            print(rendered)
        except UnicodeEncodeError:
            self.ascii_mode = True
            rendered_ascii = self.render(raw_input, affinity_result, telemetry, validation_report)
            print(rendered_ascii.encode("ascii", errors="replace").decode("ascii"))

    def render_monochrome_html(
        self,
        raw_input: str,
        affinity_result: AffinityAnalysisResult,
        telemetry: ThermalInterlockTelemetry,
        validation_report: ValidationReport,
    ) -> str:
        """Export high-contrast monochrome HTML report (solid #000000 on #FFFFFF)."""
        rendered_text = self.render(raw_input, affinity_result, telemetry, validation_report)
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Bio-Sieve Telemetry Report</title>
<style>
  body {{
    background-color: #FFFFFF;
    color: #000000;
    font-family: 'Courier New', Courier, monospace;
    margin: 20px;
    padding: 0;
  }}
  pre {{
    background-color: #FFFFFF;
    color: #000000;
    border: 2px solid #000000;
    padding: 16px;
    font-size: 13px;
    line-height: 1.35;
    white-space: pre;
    box-shadow: 4px 4px 0px #000000;
  }}
</style>
</head>
<body>
<pre>{rendered_text}</pre>
</body>
</html>"""
        return html
