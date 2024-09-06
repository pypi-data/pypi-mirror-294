import logging
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Optional
from MPSPlots.styles import mps
from dataclasses import dataclass, field
from FlowCyPy.gaussian_pulse import GaussianPulse
from FlowCyPy.scatterer_distribution import ScattererDistribution
from FlowCyPy.detector import Detector
from FlowCyPy.source import Source
from tabulate import tabulate
from FlowCyPy import ureg

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(message)s'
)

@dataclass
class FlowCytometer:
    """
    A class to simulate flow cytometer signals for Forward Scatter (FSC) and Side Scatter (SSC) channels.

    This class models the particle distribution, flow characteristics, and detector configurations to
    simulate the signal generated as particles pass through the flow cytometer's laser.

    Attributes
    ----------
    flow_area : float
        The cross-sectional area of the particle flow (in square meters).
    flow_speed : float
        The speed of the particle flow (in meters per second).
    total_time : float
        The total simulation time (in seconds).
    scatterer_distribution : ScattererDistribution
        The distribution of particle sizes which affects scattering signals.
    source : Source
        The laser source object representing the illumination scheme.
    detectors : List[Detector]
        List of `Detector` objects representing the detectors in the system.
    seed : int, optional
        Seed for random number generation (used for reproducibility).

    Methods
    -------
    simulate_pulse()
        Simulates the signal pulses for FSC and SSC channels based on particle distribution and flow.
    plot()
        Plots the simulated signals for each detector channel.
    print_properties()
        Displays the key properties of the flow cytometer and its detectors.
    """

    flow_area: float
    flow_speed: float
    total_time: float
    scatterer_distribution: ScattererDistribution
    source: Source
    detectors: List[Detector]
    seed: Optional[int] = None

    # Internal fields initialized post-creation
    time: np.ndarray = field(init=False)
    n_events: int = field(init=False)

    def __post_init__(self) -> None:
        """
        Initialize additional parameters after class instantiation by assigning physical units to parameters,
        calculating event rates, and setting the random seed.
        """
        self._add_units_to_parameters()
        self._calculate_event_rate()

        # Set the random seed for reproducibility
        if self.seed is not None:
            np.random.seed(self.seed)
        logging.info(f"FlowCytometer initialized with an estimated {self.n_events} events.")

    def _add_units_to_parameters(self) -> None:
        """Adds physical units to the core parameters of the FlowCytometer."""
        self.flow_speed *= ureg('meter/second')
        self.total_time *= ureg.second
        self.flow_area *= ureg.meter**2

    def _calculate_event_rate(self) -> None:
        """Calculates the estimated number of particle events based on the flow and particle density."""
        dt = self.total_time.to('second')
        self.rate_of_particle = self.scatterer_distribution.particle_density * self.flow_speed * self.flow_area
        self.n_events = int((self.rate_of_particle * dt).magnitude)

    def print_properties(self) -> None:
        """Displays the core properties of the flow cytometer and its detectors using the `tabulate` library."""
        properties = [
            ["Flow Speed", f"{self.flow_speed:.2f~#P}"],
            ["Total Simulation Time", f"{self.total_time:.2f~#P}"],
            ["Random Seed", self.seed if self.seed is not None else "Not set"],
            ["Estimated Number of Events", self.n_events]
        ]

        self.scatterer_distribution.print_properties()
        print("\nFlowCytometer Properties")
        print(tabulate(properties, headers=["Property", "Value"], tablefmt="grid"))

        self.source.print_properties()

        for detector in self.detectors:
            detector.print_properties()

    def simulate_pulse(self) -> None:
        """
        Simulates the signal pulses for the FSC and SSC channels by generating Gaussian pulses for
        each particle event and distributing them across the detectors.
        """
        logging.debug("Starting pulse simulation.")
        self.scatterer_distribution.generate_size(self.n_events)
        sizes_distribution = self.scatterer_distribution.sizes
        coupling_values = self.scatterer_distribution.size_coupling_factor

        for detector in self.detectors:
            time_points = int((detector.acquisition_frequency * self.total_time).to('dimensionless').magnitude)
            time = np.linspace(0, self.total_time.magnitude, time_points) * ureg.second
            raw_signal = np.zeros(time_points)

            for size, coupling in zip(sizes_distribution.magnitude, coupling_values):
                center, height, width = self._generate_pulse_parameters()
                height *= size * coupling
                pulse = GaussianPulse(center, height, width)
                raw_signal += pulse.generate(time.magnitude)

            detector.capture_signal(time=time, raw_signal=raw_signal)

    def _generate_pulse_parameters(self) -> Tuple[float, float, float]:
        """
        Generates random parameters for a Gaussian pulse, including the center, height, and width.

        Returns
        -------
        center : float
            The center of the pulse in time.
        height : Quantity
            The height of the pulse (in volts).
        width : float
            The width of the pulse (standard deviation of the Gaussian, in seconds).
        """
        center = np.random.uniform(0, self.total_time.magnitude)
        height = np.random.uniform(100, 1000) * ureg.volt
        width = np.random.uniform(0.05, 0.2) / 10  # Pulse width scaling
        return center, height, width

    def _add_to_ax(self, ax: plt.Axes) -> None:
        """
        Plots the signal for each detector channel on the given axis.

        Parameters
        ----------
        ax : plt.Axes
            The Matplotlib axis where the signal will be plotted.
        """
        ax.set(
            title='Simulated raw flow-cytometry signal',
            xlabel='Time [seconds]',
            ylabel='Signal Intensity [V]'
        )

        for c, detector in enumerate(self.detectors):
            detector._add_to_ax(ax=ax, color=f'C{c}')

        ax.legend()

    def plot(self) -> None:
        """Plots the signals generated for each detector channel."""
        logging.info(f"Plotting the signal for the different channels.")

        with plt.style.context(mps):
            fig, ax = plt.subplots(2, 1, figsize=(10, 6))

            self._add_to_ax(ax=ax[0])
            self.scatterer_distribution._add_to_ax(ax=ax[1])

            plt.show()
