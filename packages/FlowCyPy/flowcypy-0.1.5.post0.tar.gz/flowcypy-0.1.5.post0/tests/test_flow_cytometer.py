import numpy as np
import pytest
from FlowCyPy import FlowCytometer
import matplotlib.pyplot as plt
from unittest.mock import patch

def test_flow_cytometer_simulation():
    """Test the simulation of flow cytometer signals."""
    cytometer = FlowCytometer(
        particle_density=1e6,
        flow_speed=80e-6,
        flow_area=1,
        total_time=8,
        acquisition_frequency=1e3,
        noise_level=300,
        baseline_shift=0.01,
        saturation_level=100_000,
        n_bins=100,
    )
    cytometer.simulate_pulse()

    # Check that the signals are not all zeros (pulses should add non-zero values)
    assert np.any(cytometer.fsc_raw_signal > 0), "FSC signal is all zeros."
    assert np.any(cytometer.ssc_raw_signal > 0), "SSC signal is all zeros."

    # Check that the noise has been added to the signal
    assert np.var(cytometer.fsc_raw_signal) > 0, "FSC signal variance is zero, indicating no noise added."
    assert np.var(cytometer.ssc_raw_signal) > 0, "SSC signal variance is zero, indicating no noise added."

@patch('matplotlib.pyplot.show')
def test_flow_cytometer_plot(mock_show):
    """Test the plotting of flow cytometer signals."""
    cytometer = FlowCytometer(
        particle_density=1e6,
        flow_speed=80e-6,
        flow_area=1,
        total_time=8,
        acquisition_frequency=1e3,
        noise_level=300,
        baseline_shift=0.01,
        saturation_level=100_000,
        n_bins=100,
    )
    cytometer.simulate_pulse()

    cytometer.plot()

    plt.close()

    cytometer.print_properties()

if __name__ == '__main__':
    pytest.main([__file__])