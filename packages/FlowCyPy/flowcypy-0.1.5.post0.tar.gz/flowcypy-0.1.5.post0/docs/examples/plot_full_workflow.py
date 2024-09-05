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
from FlowCyPy import ScattererDistribution
from FlowCyPy import PulseAnalyzer

scatterer_distribution = ScattererDistribution(
    mean_size=10e-6,
    std_size=8e-7,
    distribution_type='normal'
)

# Create a FlowCytometer instance
cytometer = FlowCytometer(
    particle_density=10e6,
    flow_speed=80e-6,
    flow_area=1,
    total_time=0.5,
    acquisition_frequency=1e4,
    noise_level=0,
    baseline_shift=0.0,
    saturation_level=1_000,
    n_bins=1000,
)

cytometer.simulate_pulse()
cytometer.print_properties()
cytometer.plot()

# Create a PulseAnalyzer instance
analyzer = PulseAnalyzer(
    time=cytometer.time.magnitude,
    signal=cytometer.fsc_raw_signal.magnitude,
    height_threshold=0.9
)

analyzer.find_peaks()

# Calculate the widths and areas of the detected peaks
analyzer.calculate_widths()
analyzer.calculate_areas()

# Display the extracted features
analyzer.display_features()

