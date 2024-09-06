"""
Simulating Flow Cytometer Signals
==================================

This example demonstrates how to simulate signals from a flow cytometer using
the `FlowCytometer` class.

Flow cytometers generate signals (e.g., forward scatter and side scatter) when
particles pass through a laser beam. These signals can be analyzed to obtain
information about the size, complexity, and other properties of the particles.
"""

# Import the necessary libraries
from FlowCyPy import FlowCytometer, ScattererDistribution, Detector, Source


scatterer_distribution = ScattererDistribution(
    particle_density=1e12,
    mean_size=1e-6,
    std_size=1e-7,
    distribution_type='uniform'
)

source = Source(
    wavelength=1550e-9,
    optical_power=1e-3,
)

detector_0 = Detector(
    name='FSC',
    acquisition_frequency=1e3,
    noise_level=0,
    saturation_level=1_000,
    baseline_shift=0.0,
    n_bins=100,
)

detector_1 = Detector(
    name='FCC',
    acquisition_frequency=1e3,
    noise_level=0,
    saturation_level=1_000,
    baseline_shift=0.0,
    n_bins=10,
)


# scatterer_distribution.plot()

# Create a FlowCytometer instance
cytometer = FlowCytometer(
    source=source,
    flow_speed=80e-6,
    flow_area=1e-6,
    total_time=8,
    scatterer_distribution=scatterer_distribution,
    detectors=[detector_0, detector_1]
)

# Simulate the flow cytometer signals
cytometer.simulate_pulse()
cytometer.print_properties()

# Plot the generated signals
cytometer.plot()

##############################################################################
# The above plot shows simulated raw signals for both Forward Scatter (FSC) and
# Side Scatter (SSC) channels. The signals include realistic features such as
# noise, baseline shifts, and saturation effects.
#
# These signals can be used as a basis for developing and testing signal
# processing algorithms in flow cytometry.
