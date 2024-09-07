# test_scatterer_distribution.py

import pytest
from unittest.mock import patch
import matplotlib.pyplot as plt
import numpy as np
from FlowCyPy.scatterer_distribution import ScattererDistribution
from FlowCyPy.flow import Flow


@pytest.fixture
def default_flow():
    return  Flow(
        flow_speed=80e-6,
        flow_area=1e-6,
        total_time=1.0,
        mean_flow_rate=1e-6,
        std_flow_rate=0.2e-6,
        scatterer_density=1e15
    )

def test_invalid_distribution_type(default_flow):
    """Test that an invalid distribution type raises a ValueError."""
    with pytest.raises(ValueError, match="Invalid distribution type"):
        dist = ScattererDistribution(
            flow=default_flow,
            refractive_index=1.5,
            mean_size=1e-6,
            std_size=0.2e-6,
            distribution_type='invalid'
        )


@pytest.mark.parametrize('distribution_type', ['normal', 'lognormal', 'uniform', 'singular:1e-6'])
@patch('matplotlib.pyplot.show')
def test_generate_distribution_size(mock_show, distribution_type, default_flow):
    """Test if the distribution generates sizes correctly."""
    distribution = ScattererDistribution(
        flow=default_flow,
        refractive_index=1.5,
        mean_size=1e-6,
        std_size=0.2e-6,
        distribution_type=distribution_type
    )

    # Assert correct shape of generated sizes
    assert distribution.sizes.size > 0, "Generated size array has incorrect shape."

    # Assert that all sizes are positive
    assert np.all(distribution.sizes.magnitude > 0), "Some generated sizes are not positive."

    # Assert correct mean of generated sizes
    expected_mean = np.mean(distribution.sizes.magnitude)
    measure_mean = distribution.mean_size.magnitude

    assert np.isclose(expected_mean, measure_mean, atol=1e-7), (
        f"Mean of generated sizes is not close to expected mean. "
        f"Expected: {measure_mean}, but got: {expected_mean}"
    )

    # Check if size values are within expected range for specific distributions
    if distribution_type == 'normal':
        assert np.all((distribution.sizes.magnitude > 0) & (distribution.sizes.magnitude < 3e-6)), "Sizes in 'normal' distribution are out of expected bounds."
    elif distribution_type == 'lognormal':
        assert np.all(distribution.sizes.magnitude > 0), "Lognormal distribution generated non-positive sizes."
    elif distribution_type == 'uniform':
        lower_bound = distribution.mean_size.magnitude - distribution.std_size.magnitude
        upper_bound = distribution.mean_size.magnitude + distribution.std_size.magnitude
        assert np.all((distribution.sizes.magnitude >= lower_bound) & (distribution.sizes.magnitude <= upper_bound)), (
            "Sizes in 'uniform' distribution are out of expected bounds."
        )
    elif distribution_type.startswith('singular:'):
        singular_value = float(distribution_type.split(':')[1])
        assert np.all(distribution.sizes.magnitude == singular_value), (
            f"All sizes in 'singular' distribution should be {singular_value}, but got varying sizes."
        )

    # Test plotting (this will call matplotlib, but won't display it due to mock)
    distribution.plot(bins=45)

    plt.close()


def test_generate_longitudinal_positions(default_flow):
    """Test the generation of longitudinal positions based on Poisson process."""
    n_samples = 1000

    distribution = ScattererDistribution(
        refractive_index=1.5,
        flow=default_flow,
        mean_size=1e-6,
        std_size=0.2e-6,
        distribution_type='normal',
    )

    # Assert correct shape of generated longitudinal positions
    assert distribution.flow.longitudinal_positions.size > 0, "Generated longitudinal positions array has incorrect shape."

    # Assert that longitudinal positions are increasing (since they are cumulative)
    assert np.all(np.diff(distribution.flow.longitudinal_positions.magnitude) >= 0), "Longitudinal positions are not monotonically increasing."

    # Assert that no positions are negative
    assert np.all(distribution.flow.longitudinal_positions.magnitude >= 0), "Some longitudinal positions are negative."


def test_plot_positions(default_flow):
    """Test the plotting of longitudinal positions."""
    n_samples = 1000

    distribution = ScattererDistribution(
        refractive_index=1.5,
        flow=default_flow,
        mean_size=1e-6,
        std_size=0.2e-6,
        distribution_type='normal',
    )

    # Plotting the positions (mocked plt.show)
    with patch('matplotlib.pyplot.show'):
        distribution.plot(bins=45)

    plt.close()


if __name__ == '__main__':
    pytest.main([__file__])
