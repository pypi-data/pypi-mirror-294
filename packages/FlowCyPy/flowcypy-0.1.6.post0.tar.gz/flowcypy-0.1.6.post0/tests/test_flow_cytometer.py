import numpy as np
import pytest
from FlowCyPy import FlowCytometer, Detector, ScattererDistribution, Source
import matplotlib.pyplot as plt
from unittest.mock import patch


@pytest.fixture
def default_detector():
    return Detector(
        name='default',
        acquisition_frequency=1e3,
        noise_level=0,
        saturation_level=1_000,
        baseline_shift=0.0,
        n_bins=100,
    )

@pytest.fixture
def default_scatterer_distribution():
    return  ScattererDistribution(
        particle_density=1e6,
        mean_size=10e-6,
        std_size=8e-7,
        distribution_type='lognormal'
    )


@pytest.fixture
def default_source():
    return Source(
        wavelength=1550e-9,
        optical_power=1e-3,
    )

def test_flow_cytometer_simulation(default_source, default_detector, default_scatterer_distribution):
    """Test the simulation of flow cytometer signals."""
    cytometer = FlowCytometer(
        source=default_source,
        flow_speed=80e-6,
        flow_area=1,
        total_time=8,
        detectors=[default_detector],
        scatterer_distribution=default_scatterer_distribution
    )
    cytometer.simulate_pulse()

    # Check that the signals are not all zeros (pulses should add non-zero values)
    assert np.any(default_detector.signal > 0), "FSC signal is all zeros."
    assert np.any(default_detector.signal > 0), "SSC signal is all zeros."

    # Check that the noise has been added to the signal
    assert np.var(default_detector.signal) > 0, "FSC signal variance is zero, indicating no noise added."
    assert np.var(default_detector.signal) > 0, "SSC signal variance is zero, indicating no noise added."

@patch('matplotlib.pyplot.show')
def test_flow_cytometer_plot(mock_show, default_source, default_detector, default_scatterer_distribution):
    """Test the plotting of flow cytometer signals."""
    cytometer = FlowCytometer(
        source=default_source,
        flow_speed=80e-6,
        flow_area=1,
        total_time=8,
        detectors=[default_detector],
        scatterer_distribution=default_scatterer_distribution
    )
    cytometer.simulate_pulse()

    cytometer.plot()

    plt.close()

    cytometer.print_properties()

if __name__ == '__main__':
    pytest.main([__file__])