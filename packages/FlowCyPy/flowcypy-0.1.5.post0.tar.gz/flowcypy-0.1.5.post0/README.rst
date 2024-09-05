FlowCyPy Simulation Tool
========================

|logo|

|python| |coverage| |PyPi| |PyPi_download| |docs|

Overview
--------

The **FlowCytometer Simulation Tool** is a Python-based simulation framework designed to replicate the operation of a flow cytometer. It generates realistic raw signals for Forward Scatter (FSC) and Side Scatter (SSC) channels, incorporating noise, baseline shifts, signal saturation, and signal discretization into a specified number of bins. This tool is highly configurable, allowing users to simulate a wide range of scenarios and analyze the resulting signals.

Features
--------

- **Simulate Particle Events**: Generate realistic FSC and SSC signals based on user-defined particle event parameters.
- **Noise and Baseline Shift**: Introduce Gaussian noise and sinusoidal baseline shifts to simulate real-world conditions.
- **Signal Saturation**: Apply saturation effects to replicate detector limits.
- **Signal Discretization**: Discretize the continuous signal into a specified number of bins for quantized signal analysis.
- **Flexible Plotting**: Visualize the simulated signals with customizable options for plotting specific channels or both together.

Installation
------------

To install the `FlowCytometer` simulation tool, you can clone the repository and install the required dependencies:

.. code-block:: bash

    git clone https://github.com/MartinPdeS/FlowCyPy.git
    cd FlowCyPy
    pip install .[testing]

Dependencies
------------

- `numpy`: For numerical operations and signal generation.
- `matplotlib`: For plotting the simulated signals.
- `scipy`: A module to generate Gaussian pulses (part of this package or an external dependency).

Getting Started
---------------

Below is a quick guide on how to get started with the `FlowCytometer` simulation tool.


.. code-block:: python

    # Import the necessary libraries
    from FlowCyPy import FlowCytometer
    from FlowCyPy import ScattererDistribution

    scatterer_distribution = ScattererDistribution(
        mean_size=1e-6,
        std_size=1e-7,
        distribution_type='normal'
    )

    # Create a FlowCytometer instance
    cytometer = FlowCytometer(
        particle_density=1e6,
        flow_speed=80e-6,
        flow_area=1,
        total_time=8,
        acquisition_frequency=1e3,
        noise_level=30,
        baseline_shift=0.01,
        saturation_level=1_000,
        n_bins=100,

    )

    # Simulate the flow cytometer signals
    cytometer.simulate_pulse()
    cytometer.print_properties()

    # Plot the generated signals
    cytometer.plot()

This produce the following figure:
|example_fcm|


Plenty of other examples are available online, I invite you to check the `examples <https://FlowCytometry.readthedocs.io/en/master/gallery/index.html>`_
section of the documentation.

Contact Information
************************
As of 2024, the project is still under development. If you want to collaborate, it would be a pleasure! I encourage you to contact me.

FlowCyPy was written by `Martin Poinsinet de Sivry-Houle <https://github.com/MartinPdS>`_  .

Email:`martin.poinsinet.de.sivry@gmail.ca <mailto:martin.poinsinet.de.sivry@gmail.ca?subject=FlowCyPy>`_ .


.. |python| image:: https://img.shields.io/pypi/pyversions/flowcypy.svg
   :target: https://www.python.org/

.. |logo| image:: https://github.com/MartinPdeS/FlowCyPy/raw/master/docs/images/logo.png

.. |example_fcm| image:: https://github.com/MartinPdeS/FlowCyPy/blob/master/docs/images/example_signal_FCM.png

.. |coverage| image:: https://raw.githubusercontent.com/MartinPdeS/FlowCyPy/python-coverage-comment-action-data/badge.svg
   :alt: Unittest coverage
   :target: https://htmlpreview.github.io/?https://github.com/MartinPdeS/FlowCyPy/blob/python-coverage-comment-action-data/htmlcov/index.html

.. |PyPi| image:: https://badge.fury.io/py/FlowCyPy.svg
    :target: https://badge.fury.io/py/FlowCyPy

.. |PyPi_download| image:: https://img.shields.io/pypi/dm/FlowCyPy.svg
    :target: https://pypistats.org/packages/flowcypy

.. |docs| image:: https://readthedocs.org/projects/flowcytometry/badge/?version=latest
    :target: https://flowcytometry.readthedocs.io/en/latest/