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
from FlowCyPy import FlowCytometer

# Create a FlowCytometer instance
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
