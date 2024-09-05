# test_scatterer_distribution.py

import pytest
import numpy as np
from pint import UnitRegistry
from FlowCyPy.scatterer_distribution import ScattererDistribution

# Initialize a unit registry
ureg = UnitRegistry()

@pytest.fixture
def default_scatterer_distribution():
    """Fixture to create a default ScattererDistribution object."""
    return ScattererDistribution(
        mean_size=1e-6,
        std_size=0.2e-6,
        distribution_type='normal'
    )

@pytest.fixture
def lognormal_scatterer_distribution():
    """Fixture to create a ScattererDistribution with a lognormal distribution."""
    return ScattererDistribution(
        mean_size=1e-6,
        std_size=0.2e-6,
        distribution_type='lognormal'
    )

@pytest.fixture
def uniform_scatterer_distribution():
    """Fixture to create a ScattererDistribution with a uniform distribution."""
    return ScattererDistribution(
        mean_size=1e-6,
        std_size=0.2e-6,
        distribution_type='uniform'
    )

def test_generate_normal_distribution_size(default_scatterer_distribution):
    """Test if the normal distribution generates sizes correctly."""
    n_samples = 1000
    sizes = default_scatterer_distribution.generate_size(n_samples)

    assert sizes.shape == (n_samples,), "Generated size array has incorrect shape."

    expected_mean = np.mean(sizes.magnitude)
    measure_mean = default_scatterer_distribution.mean_size.magnitude
    assert np.isclose(expected_mean, measure_mean, atol=1e-7), "Mean of generated sizes is not close to expected mean."

    expected_std = np.std(sizes.magnitude)
    measure_std = default_scatterer_distribution.std_size.magnitude

    assert np.isclose(expected_std, measure_std, atol=1e-7), "Standard deviation of generated sizes is not close to expected standard deviation."

def test_generate_lognormal_distribution_size(lognormal_scatterer_distribution):
    """Test if the lognormal distribution generates sizes correctly."""
    n_samples = 1000
    sizes = lognormal_scatterer_distribution.generate_size(n_samples)

    assert sizes.shape == (n_samples,), "Generated size array has incorrect shape."
    assert np.all(sizes.magnitude > 0), "Lognormal distribution should not generate negative sizes."

def test_generate_uniform_distribution_size(uniform_scatterer_distribution):
    """Test if the uniform distribution generates sizes correctly."""
    n_samples = 1000
    sizes = uniform_scatterer_distribution.generate_size(n_samples)
    mean_size = uniform_scatterer_distribution.mean_size.magnitude
    std_size = uniform_scatterer_distribution.std_size.magnitude

    assert sizes.shape == (n_samples,), "Generated size array has incorrect shape."
    assert np.all(sizes.magnitude >= (mean_size - std_size)), "Uniform distribution generated values below expected range."
    assert np.all(sizes.magnitude <= (mean_size + std_size)), "Uniform distribution generated values above expected range."

def test_invalid_distribution_type():
    """Test that an invalid distribution type raises a ValueError."""
    with pytest.raises(ValueError, match="Invalid distribution type. Choose 'normal', 'lognormal', or 'uniform'."):
        dist = ScattererDistribution(mean_size=1e-6, std_size=0.2e-6, distribution_type='invalid')
        dist.generate_size(100)

def test_generate_size_with_zero_samples(default_scatterer_distribution):
    """Test that generate_size works with zero samples."""
    sizes = default_scatterer_distribution.generate_size(0)
    assert sizes.size == 0, "Expected an empty array when generating zero samples."

if __name__ == '__main__':
    pytest.main([__file__])