"""
Simulating and Analyzing Flow Cytometer Signals
===============================================

This script demonstrates how to simulate flow cytometer signals using the `FlowCytometer` class
and analyze the results using the `PulseAnalyzer` class from the `FlowCyPy` library.

Flow cytometers measure forward scatter (FSC) and side scatter (SSC) signals when particles pass through a laser beam,
providing information about particle size, complexity, and other characteristics.

Steps in this Workflow:
-----------------------
1. Define a particle size distribution using `ScattererDistribution`.
2. Simulate flow cytometer signals using `FlowCytometer`.
3. Analyze the forward scatter signal with `PulseAnalyzer` to extract features like peak height, width, and area.
4. Visualize the generated signals and display the extracted pulse features.
"""

# Step 1: Import necessary modules from FlowCyPy
from FlowCyPy import FlowCytometer, ScattererDistribution, PulseAnalyzer, Detector, Source

# Step 2: Define the particle size distribution
# ---------------------------------------------
# Using a lognormal size distribution with a mean of 10 µm and a standard deviation of 0.8 µm.
scatterer_distribution = ScattererDistribution(
    particle_density=10e6,         # 10 million particles per cubic meter
    mean_size=10e-6,               # Mean particle size: 10 µm
    std_size=8e-7,                 # Standard deviation: 0.8 µm
    distribution_type='lognormal'  # Lognormal distribution
)

source = Source(
    wavelength=1550e-9,    # Wavelenght of the laser source: 1550 nm
    optical_power=200e-3,  # Optical power of the laser source: 200 milliwatt
)

detector = Detector(
    name='first detector',
    acquisition_frequency=1e4,  # Sampling frequency: 10,000 Hz
    noise_level=0.00,           # Signal noise level: 0.5 volts
    baseline_shift=0.00,        # Signal noise level: 0.5 volts
    saturation_level=1e3,       # Signal saturation at 1000 volts
    n_bins=1024                 # Discretization bins: 1024
)

# Step 3: Simulate Flow Cytometer Signals
# ---------------------------------------
# Create a FlowCytometer instance to simulate FSC/SSC signals with defined parameters.
cytometer = FlowCytometer(
    source=source,
    flow_speed=80e-6,                # Flow speed: 80 µm/s
    flow_area=1,                     # Flow area: 1 m²
    total_time=0.5,                  # Simulation time: 0.5 seconds
    scatterer_distribution=scatterer_distribution,  # Using the defined particle size distribution
    detectors=[detector]             # Detectors to add to the system
)

# Generate simulated pulses for the FSC and SSC channels
cytometer.simulate_pulse()

# Display the properties of the simulated cytometer
cytometer.print_properties()

# Visualize the generated signals
cytometer.plot()

# Step 4: Analyze the Simulated FSC Signal
# ----------------------------------------
# Create a PulseAnalyzer to extract features like peak height, width, and area from the FSC signal.
analyzer = PulseAnalyzer(
    detector=detector,        # Time detector to analyze the signal from
    height_threshold=None     # Threshold for detecting peaks
)

# # Run the analysis to detect and measure pulse features
analyzer.run()

analyzer.plot()

# # Display the extracted peak features such as height, width, and area
analyzer.display_features()

"""
Summary:
--------
This script simulates flow cytometer signals, processes them to detect peaks in the forward scatter channel,
and extracts important features. The process is visualized through signal plots, and key properties are displayed.
"""
