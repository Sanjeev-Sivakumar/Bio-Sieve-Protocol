"""Runtime Physics and Interlock Simulator Module (Module 2).

Decentralized Air-Gapped Bio-Sieve Protocol — Offline Simulation & Telemetry Framework.

Mathematical Modeling:
1. Microfluidic Channel Specifications (Hypothetical Simulation):
   - Channel Length (L_channel): 50.0 micrometers (50e-6 m).
   - Hydraulic Diameter (D_H): 12.0 micrometers (12e-6 m).
   - Ambient Reference Temp (T_ambient): 295.15 K (22.0 °C).
   - Fluid Density (rho): 1050.0 kg/m^3 (aqueous carrier buffer).
   - Dynamic Viscosity (mu): 1.002e-3 Pa*s (20 °C water equivalent).

2. Core Thermal Gradient:
   - Dissipated Thermal Energy: delta_T_diss = (len(input) % 120) / 20.0 + (entropy * 4.25) [K]
   - Core Temperature: T_core = T_ambient + delta_T_diss [K]
   - Thermal Gradient: Delta_T = (T_core - T_ambient) / L_channel [K / micrometer]

3. Flow Reynolds Number:
   - Velocity: v = v_base * (1.0 + 0.005 * min(N, 1000)) * (1.0 + 0.1 * (H_norm - 0.5)) [m/s]
   - Re = (rho * v * D_H) / mu
   - Regimes: Laminar (Re < 2300), Transitional (2300 <= Re < 4000), Turbulent (Re >= 4000)

4. Kinetic Rearrangement Probability:
   - Logistic Boltzmann-like model:
     xi = 0.45 * Delta_T + 0.0008 * Re + 0.35 * H_norm - 1.80
     P_rearrange = 1.0 / (1.0 + exp(-xi))   [strictly bounded in [0.0, 1.0]]

5. Session Interlock:
   - States: ARMED (nominal) vs TRIPPED (safety threshold breached).
   - When tripped, subsequent executions are halted until reset_interlock() is called.
   - DISCLAIMER: This is a purely computational physics simulation. It never issues commands to physical hardware.
"""

from __future__ import annotations

import math
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple


class InterlockState(str, Enum):
    """Session-local interlock state."""
    ARMED = "ARMED"
    TRIPPED = "TRIPPED"


class FlowRegime(str, Enum):
    """Fluid flow hydrodynamic classification."""
    LAMINAR = "LAMINAR"
    TRANSITIONAL = "TRANSITIONAL"
    TURBULENT = "TURBULENT"


@dataclass(frozen=True)
class ChannelConstants:
    """Explicitly documented physical constants for the hypothetical microchannel."""
    channel_length_um: float = 50.0             # 50.0 micrometers
    hydraulic_diameter_um: float = 12.0          # 12.0 micrometers
    ambient_temp_k: float = 295.15              # 22.0 °C
    carrier_density_kg_m3: float = 1050.0       # kg/m^3
    carrier_viscosity_pa_s: float = 1.002e-3    # Pa * s (at 20 °C)
    base_velocity_m_s: float = 0.12             # Nominal channel entrance velocity
    base_pressure_kpa: float = 101.325          # 1 atm base atmospheric pressure


@dataclass(frozen=True)
class SafetyThresholds:
    """Operational safety thresholds that trigger hardware interlock override."""
    max_reynolds_number: float = 3200.0         # Upper limit before shear instability
    max_thermal_gradient_k_um: float = 0.85     # Max allowed gradient [K / um]
    max_core_temp_c: float = 65.0               # Max core nozzle temperature [°C]
    max_rearrangement_prob: float = 0.8200      # Max probability threshold [0.0 - 1.0]


@dataclass
class InterlockTriggerRecord:
    """Audit record capturing the exact measurement that tripped the interlock."""
    parameter_name: str
    observed_value: float
    threshold_value: float
    unit: str
    timestamp_utc: str
    description: str


@dataclass
class ThermalInterlockTelemetry:
    """Real-time calculated physics and interlock telemetry."""
    input_length: int
    ambient_temp_c: float
    core_temp_c: float
    core_temp_k: float
    thermal_gradient_k_um: float
    flow_velocity_m_s: float
    reynolds_number: float
    flow_regime: FlowRegime
    pressure_drop_kpa: float
    total_pressure_kpa: float
    rearrangement_probability: float
    interlock_state: InterlockState
    is_safe: bool
    trigger_records: List[InterlockTriggerRecord]
    assumed_parameters: Dict[str, Any]
    inferred_parameters: Dict[str, Any]
    execution_time_ms: float


class RuntimePhysicsSimulator:
    """Simulates microsecond thermal-fluidic dynamics and enforces session safety interlocks."""

    def __init__(
        self,
        constants: Optional[ChannelConstants] = None,
        thresholds: Optional[SafetyThresholds] = None,
    ) -> None:
        """Initialize the simulator with constants and safety thresholds."""
        self.constants = constants or ChannelConstants()
        self.thresholds = thresholds or SafetyThresholds()
        self._interlock_state: InterlockState = InterlockState.ARMED
        self._trip_history: List[InterlockTriggerRecord] = []

    @property
    def interlock_state(self) -> InterlockState:
        """Current session-local interlock state."""
        return self._interlock_state

    @property
    def trip_history(self) -> List[InterlockTriggerRecord]:
        """Historical list of interlock triggers."""
        return list(self._trip_history)

    def reset_interlock(self) -> None:
        """Explicitly reset the simulated interlock back to ARMED state."""
        self._interlock_state = InterlockState.ARMED
        self._trip_history.clear()

    def simulate(
        self,
        input_length: int,
        shannon_entropy: float,
        normalized_entropy: float = 0.5,
    ) -> ThermalInterlockTelemetry:
        """Compute runtime physics equations and evaluate interlock criteria.

        Args:
            input_length: Length of the input string sequence.
            shannon_entropy: Shannon entropy in bits (from Module 1).
            normalized_entropy: Normalized entropy in [0.0, 1.0].

        Returns:
            ThermalInterlockTelemetry dataclass with all computed metrics.
        """
        start_time = time.perf_counter()

        # 1. Thermal Calculations
        # Input-derived thermal dissipation scaling dynamically with sequence length and entropy:
        length_term = min(input_length, 4500) / 40.0
        entropy_boost = max(0.0, shannon_entropy) * 4.25
        delta_t_dissipation = length_term + entropy_boost

        core_temp_k = self.constants.ambient_temp_k + delta_t_dissipation
        core_temp_c = core_temp_k - 273.15
        ambient_temp_c = self.constants.ambient_temp_k - 273.15

        # Thermal gradient: Delta_T = (T_core - T_ambient) / L_channel [K / micrometer]
        thermal_gradient_k_um = delta_t_dissipation / self.constants.channel_length_um

        # 2. Fluidic Velocity & Reynolds Number
        # v = v_base * (1 + 0.005 * min(N, 1000)) * (1 + 0.1 * (H_norm - 0.5))
        length_scale = 1.0 + 0.005 * min(input_length, 1000)
        entropy_scale = 1.0 + 0.10 * (max(0.0, min(1.0, normalized_entropy)) - 0.5)
        flow_velocity_m_s = self.constants.base_velocity_m_s * length_scale * entropy_scale

        # Re = (rho * v * D_H) / mu
        # D_H in meters:
        dh_m = self.constants.hydraulic_diameter_um * 1e-6
        reynolds_number = (self.constants.carrier_density_kg_m3 * flow_velocity_m_s * dh_m) / self.constants.carrier_viscosity_pa_s

        if reynolds_number < 2300.0:
            regime = FlowRegime.LAMINAR
        elif reynolds_number < 4000.0:
            regime = FlowRegime.TRANSITIONAL
        else:
            regime = FlowRegime.TURBULENT

        # 3. Microchannel Pressure Drop (Hagen-Poiseuille)
        # Delta P = (32 * mu * L * v) / (D_H^2) [Pa]
        l_channel_m = self.constants.channel_length_um * 1e-6
        delta_p_pa = (32.0 * self.constants.carrier_viscosity_pa_s * l_channel_m * flow_velocity_m_s) / (dh_m ** 2)
        delta_p_kpa = delta_p_pa / 1000.0
        total_pressure_kpa = self.constants.base_pressure_kpa + delta_p_kpa

        # 4. Kinetic Rearrangement Probability
        # Logistic Boltzmann-like model:
        # xi = 1.20 * Delta_T + 0.015 * Re + 0.75 * H_norm - 1.80
        xi = (
            (1.20 * thermal_gradient_k_um)
            + (0.015 * reynolds_number)
            + (0.75 * normalized_entropy)
            - 1.80
        )
        # Clamped exponent to prevent overflow
        xi_clamped = max(-20.0, min(20.0, xi))
        rearrangement_prob = 1.0 / (1.0 + math.exp(-xi_clamped))

        # 5. Safety Threshold Evaluation
        new_triggers: List[InterlockTriggerRecord] = []
        now_iso = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

        if reynolds_number > self.thresholds.max_reynolds_number:
            new_triggers.append(InterlockTriggerRecord(
                parameter_name="Reynolds Number (Re)",
                observed_value=round(reynolds_number, 2),
                threshold_value=self.thresholds.max_reynolds_number,
                unit="dimensionless",
                timestamp_utc=now_iso,
                description="Hydrodynamic shear instability detected; flow exceeds laminar/transitional boundary.",
            ))

        if thermal_gradient_k_um > self.thresholds.max_thermal_gradient_k_um:
            new_triggers.append(InterlockTriggerRecord(
                parameter_name="Thermal Gradient (Delta_T)",
                observed_value=round(thermal_gradient_k_um, 4),
                threshold_value=self.thresholds.max_thermal_gradient_k_um,
                unit="K/um",
                timestamp_utc=now_iso,
                description="Channel thermal gradient exceeded safe dissipation limit.",
            ))

        if core_temp_c > self.thresholds.max_core_temp_c:
            new_triggers.append(InterlockTriggerRecord(
                parameter_name="Core Temperature (T_core)",
                observed_value=round(core_temp_c, 2),
                threshold_value=self.thresholds.max_core_temp_c,
                unit="deg C",
                timestamp_utc=now_iso,
                description="Core microchannel temperature exceeded safe denaturing ceiling.",
            ))

        if rearrangement_prob > self.thresholds.max_rearrangement_prob:
            new_triggers.append(InterlockTriggerRecord(
                parameter_name="Rearrangement Probability (P_rearrange)",
                observed_value=round(rearrangement_prob, 4),
                threshold_value=self.thresholds.max_rearrangement_prob,
                unit="prob",
                timestamp_utc=now_iso,
                description="Kinetic structural rearrangement probability exceeded safety envelope threshold.",
            ))

        is_safe = (len(new_triggers) == 0) and (self._interlock_state != InterlockState.TRIPPED)
        if len(new_triggers) > 0:
            self._interlock_state = InterlockState.TRIPPED
            self._trip_history.extend(new_triggers)

        elapsed_ms = round((time.perf_counter() - start_time) * 1000.0, 3)

        return ThermalInterlockTelemetry(
            input_length=input_length,
            ambient_temp_c=round(ambient_temp_c, 2),
            core_temp_c=round(core_temp_c, 2),
            core_temp_k=round(core_temp_k, 2),
            thermal_gradient_k_um=round(thermal_gradient_k_um, 4),
            flow_velocity_m_s=round(flow_velocity_m_s, 4),
            reynolds_number=round(reynolds_number, 2),
            flow_regime=regime,
            pressure_drop_kpa=round(delta_p_kpa, 3),
            total_pressure_kpa=round(total_pressure_kpa, 3),
            rearrangement_probability=round(rearrangement_prob, 4),
            interlock_state=self._interlock_state,
            is_safe=is_safe,
            trigger_records=list(new_triggers if not is_safe else []),
            assumed_parameters=self._get_assumed_parameters(),
            inferred_parameters={
                "delta_t_dissipation_k": round(delta_t_dissipation, 2),
                "velocity_scaling_factor": round(length_scale * entropy_scale, 3),
                "kinetic_activation_exponent": round(xi, 4),
            },
            execution_time_ms=elapsed_ms,
        )

    def _get_assumed_parameters(self) -> Dict[str, Any]:
        """Return explicitly documented physical constants assumed by the model."""
        return {
            "channel_length_um": self.constants.channel_length_um,
            "hydraulic_diameter_um": self.constants.hydraulic_diameter_um,
            "ambient_temp_k": self.constants.ambient_temp_k,
            "carrier_density_kg_m3": self.constants.carrier_density_kg_m3,
            "carrier_viscosity_pa_s": self.constants.carrier_viscosity_pa_s,
            "base_velocity_m_s": self.constants.base_velocity_m_s,
            "base_pressure_kpa": self.constants.base_pressure_kpa,
            "threshold_max_re": self.thresholds.max_reynolds_number,
            "threshold_max_gradient_k_um": self.thresholds.max_thermal_gradient_k_um,
            "threshold_max_temp_c": self.thresholds.max_core_temp_c,
            "threshold_max_rearrange_prob": self.thresholds.max_rearrangement_prob,
        }
