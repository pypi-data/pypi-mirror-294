# test_scatterer_distribution.py

import pytest
from unittest.mock import patch
import matplotlib.pyplot as plt
import numpy as np
from FlowCyPy.scatterer_distribution import ScattererDistribution


def test_invalid_distribution_type():
    """Test that an invalid distribution type raises a ValueError."""
    with pytest.raises(ValueError, match="Invalid distribution type. Choose 'normal', 'lognormal', or 'uniform'."):
        dist = ScattererDistribution(
            particle_density=1e6,
            mean_size=1e-6,
            std_size=0.2e-6,
            distribution_type='invalid'
        )

        dist.generate_size(100)


@pytest.mark.parametrize('distribution_type', ['normal', 'lognormal', 'uniform'])
@patch('matplotlib.pyplot.show')
def test_generate_distribution_size(mock_show, distribution_type):
    """Test if the distribution generates sizes correctly."""
    n_samples = 1000

    distribution = ScattererDistribution(
        particle_density=1e6,
        mean_size=1e-6,
        std_size=0.2e-6,
        distribution_type=distribution_type
    )

    distribution.generate_size(n_samples)

    assert distribution.sizes.shape == (n_samples,), "Generated size array has incorrect shape."

    expected_mean = np.mean(distribution.sizes.magnitude)
    measure_mean = distribution.mean_size.magnitude

    assert np.isclose(expected_mean, measure_mean, atol=1e-7), "Mean of generated sizes is not close to expected mean."

    distribution.plot(bins=45)

    plt.close()


if __name__ == '__main__':
    pytest.main([__file__])