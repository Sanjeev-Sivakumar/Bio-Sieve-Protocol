"""Unit tests for Module 2: Runtime Physics and Interlock Simulator."""

import unittest
from thermal_interlock import (
    ChannelConstants,
    InterlockState,
    RuntimePhysicsSimulator,
    SafetyThresholds,
)


class TestThermalInterlockSimulator(unittest.TestCase):
    """Test suite for RuntimePhysicsSimulator."""

    def setUp(self) -> None:
        self.simulator = RuntimePhysicsSimulator()

    def test_nominal_simulation(self) -> None:
        """Verify normal sequence yields ARMED interlock and valid physical units."""
        telemetry = self.simulator.simulate(
            input_length=60,
            shannon_entropy=1.85,
            normalized_entropy=0.75,
        )
        self.assertEqual(telemetry.interlock_state, InterlockState.ARMED)
        self.assertTrue(telemetry.is_safe)
        self.assertGreater(telemetry.core_temp_c, telemetry.ambient_temp_c)
        self.assertGreater(telemetry.reynolds_number, 0.0)
        self.assertTrue(0.0 <= telemetry.rearrangement_probability <= 1.0)
        self.assertEqual(len(telemetry.trigger_records), 0)

    def test_thermal_gradient_calculation(self) -> None:
        """Verify thermal gradient equation: delta_T = (T_core - T_ambient) / L_channel."""
        telemetry = self.simulator.simulate(
            input_length=100,
            shannon_entropy=2.0,
            normalized_entropy=1.0,
        )
        expected_gradient = (telemetry.core_temp_k - self.simulator.constants.ambient_temp_k) / self.simulator.constants.channel_length_um
        self.assertAlmostEqual(telemetry.thermal_gradient_k_um, expected_gradient, places=3)

    def test_reynolds_number_calculation(self) -> None:
        """Verify Reynolds number equation: Re = (rho * v * D_H) / mu."""
        telemetry = self.simulator.simulate(
            input_length=80,
            shannon_entropy=1.5,
            normalized_entropy=0.6,
        )
        dh_m = self.simulator.constants.hydraulic_diameter_um * 1e-6
        expected_re = (
            self.simulator.constants.carrier_density_kg_m3
            * telemetry.flow_velocity_m_s
            * dh_m
        ) / self.simulator.constants.carrier_viscosity_pa_s
        self.assertAlmostEqual(telemetry.reynolds_number, expected_re, places=1)

    def test_interlock_tripping_on_stress(self) -> None:
        """Verify interlock transitions to TRIPPED when extreme conditions are simulated."""
        strict_thresholds = SafetyThresholds(
            max_reynolds_number=100.0,  # Artificially low limit to trigger trip
            max_thermal_gradient_k_um=0.01,
            max_core_temp_c=25.0,
            max_rearrangement_prob=0.10,
        )
        strict_simulator = RuntimePhysicsSimulator(thresholds=strict_thresholds)
        telemetry = strict_simulator.simulate(
            input_length=500,
            shannon_entropy=3.5,
            normalized_entropy=0.9,
        )
        self.assertEqual(telemetry.interlock_state, InterlockState.TRIPPED)
        self.assertFalse(telemetry.is_safe)
        self.assertGreater(len(telemetry.trigger_records), 0)

        # Ensure trip state persists on subsequent calls
        second_telemetry = strict_simulator.simulate(
            input_length=10,
            shannon_entropy=0.5,
            normalized_entropy=0.2,
        )
        self.assertEqual(second_telemetry.interlock_state, InterlockState.TRIPPED)
        self.assertFalse(second_telemetry.is_safe)

        # Reset interlock
        strict_simulator.reset_interlock()
        self.assertEqual(strict_simulator.interlock_state, InterlockState.ARMED)


if __name__ == "__main__":
    unittest.main()
