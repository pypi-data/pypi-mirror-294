
import logging
import numpy as np
import matplotlib.pyplot as plt
from MPSPlots.styles import mps
from dataclasses import dataclass, field
from pint import UnitRegistry
from FlowCyPy.gaussian_pulse import GaussianPulse
from FlowCyPy.scatterer_distribution import ScattererDistribution
from FlowCyPy.signal_processor import SignalProcessor
from tabulate import tabulate

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(message)s'
)

# Initialize a unit registry
ureg = UnitRegistry()

@dataclass
class FlowCytometer:
    """
    A dataclass to simulate the operation of a flow cytometer, generating raw signals for Forward
    Scatter (FSC) and Side Scatter (SSC) channels. The class models the signal based on particle
    distribution, flow characteristics, and acquisition parameters.

    The signals generated include noise, baseline shifts, and saturation effects, and can be further
    discretized for analysis. It uses the `pint` library for handling physical units and ensures unit
    consistency throughout the simulation.

    Attributes
    ----------
    particle_density : float
        The density of particles in the flow (particles per cubic meter).
    flow_area : float
        The cross-sectional area of the flow (in square meters).
    flow_speed : float
        The speed of the particle flow (in meters per second).
    total_time : float
        Total time for which the simulation runs (in seconds).
    acquisition_frequency : float
        The frequency at which data is sampled (in Hertz).
    scatterer_distribution : ScattererDistribution
        The distribution of particle sizes, which affects the intensity of the scattered signals.
    noise_level : float
        The level of noise added to the signal (in volts).
    baseline_shift : float
        The amplitude of baseline shifts added to the signal (in volts).
    saturation_level : float
        The maximum signal level before saturation occurs (in volts).
    n_bins : int
        The number of bins to discretize the signal into.
    seed : int, optional
        The random seed for reproducibility. If not provided, randomness is not fixed.

    Methods
    -------
    simulate_pulse()
        Simulates the pulses for FSC and SSC channels based on particle size distribution, flow characteristics,
        and acquisition parameters.
    plot(channel: str = "both")
        Plots the raw signals for FSC, SSC, or both channels, showing how the signal evolves over time.
    print_properties()
        Prints the key properties of the flow cytometer, such as particle density, flow speed, and estimated
        number of events.

    Examples
    --------
    Initialize a FlowCytometer and simulate a pulse:

    >>> flow_cytometer = FlowCytometer(particle_density=1e6, flow_area=1e-6, flow_speed=0.02, total_time=1, acquisition_frequency=1e4)
    >>> flow_cytometer.simulate_pulse()
    >>> flow_cytometer.plot()
    >>> flow_cytometer.print_properties()
    """

    # Initialization of key parameters
    particle_density: float  # particles per cubic meter
    flow_area: float  # Area of the flow of particle (in square meters)
    flow_speed: float  # Flow speed in meters per second
    total_time: float  # Total simulation time in seconds
    acquisition_frequency: float  # Acquisition frequency in Hertz
    scatterer_distribution: ScattererDistribution = field(default_factory=lambda: ScattererDistribution())
    noise_level: float = 0.05  # Noise level (volts)
    baseline_shift: float = 0.01  # Baseline shift (volts)
    saturation_level: float = 1e3  # Saturation level (volts)
    n_bins: int = 100  # Number of bins for discretization
    seed: int = None  # Random seed for reproducibility

    # Internal fields initialized later
    time: np.ndarray = field(init=False)
    fsc_raw_signal: np.ndarray = field(init=False)
    ssc_raw_signal: np.ndarray = field(init=False)

    def __post_init__(self) -> None:
        """
        Post-initialization method to add units to the parameters, calculate the number of time points,
        initialize raw signals, and estimate the number of events based on the particle density and flow characteristics.
        """
        self._add_units_to_parameters()

        # Calculate the number of time points for the simulation
        self.time_points = int((self.acquisition_frequency * self.total_time).to('dimensionless').magnitude)

        self.time = np.linspace(0, self.total_time.magnitude, self.time_points) * ureg.second

        # Initialize FSC and SSC signals as arrays of zeros with appropriate units
        self.fsc_raw_signal = np.zeros(self.time_points) * ureg.volt
        self.ssc_raw_signal = np.zeros(self.time_points) * ureg.volt

        # Estimate the number of events based on particle density, flow speed, and flow area
        dt = self.total_time.to('second')
        self.rate_of_particle = self.particle_density * self.flow_speed * self.flow_area
        self.n_events = int((self.rate_of_particle * dt).magnitude)

        # Set the random seed for reproducibility, if provided
        if self.seed is not None:
            np.random.seed(self.seed)

        logging.info(f"FlowCytometer initialized with {self.time_points} time points and estimated {self.n_events} events.")

    def _add_units_to_parameters(self) -> None:
        """
        Converts and assigns proper physical units to key parameters in the FlowCytometer.

        The following attributes are updated with their corresponding units:

        - `particle_density` (float): Converted to `particles per cubic meter`.
        - `flow_speed` (float): Converted to `meters per second`.
        - `total_time` (float): Converted to `seconds`.
        - `flow_area` (float): Converted to `square meters`.
        - `acquisition_frequency` (float): Converted to `hertz`.
        - `noise_level` (float): Converted to `volts`.
        - `baseline_shift` (float): Converted to `volts`.
        - `saturation_level` (float): Converted to `volts`.

        """
        self.particle_density *= ureg('particles/meter**3')
        self.flow_speed *= ureg('meter/second')
        self.total_time *= ureg.second
        self.flow_area *= ureg.meter**2
        self.acquisition_frequency *= ureg.hertz
        self.noise_level *= ureg.volt
        self.baseline_shift *= ureg.volt
        self.saturation_level *= ureg.volt

    def simulate_pulse(self) -> None:
        """
        Main function to simulate pulses for FSC and SSC channels.
        This function calls smaller, dedicated methods to handle different parts of the process.
        """
        logging.debug("Starting pulse simulation.")

        baseline = self._generate_baseline_shift()

        # Generate particle sizes based on the scatterer size distribution
        sizes_distribution = self.scatterer_distribution.generate_size(self.n_events)

        for size in sizes_distribution.magnitude:
            center, fsc_height, ssc_height, width = self._generate_pulse_parameters()

            # Scale pulse heights based on particle size
            fsc_height *= size * 1e6
            ssc_height *= size * 1e6

            fsc_pulse = GaussianPulse(center, fsc_height, width)
            ssc_pulse = GaussianPulse(center, ssc_height, width)

            self._accumulate_pulse_signal(fsc_pulse, ssc_pulse)

        # Use SignalProcessor to handle signal processing
        signal_processor = SignalProcessor(
            self.fsc_raw_signal,
            self.ssc_raw_signal,
            self.noise_level,
            self.baseline_shift,
            self.saturation_level,
            self.n_bins,
            self.time_points
        )
        signal_processor.add_noise_and_baseline(baseline)
        signal_processor.apply_saturation()
        signal_processor.discretize_signals()

    def _generate_baseline_shift(self) -> np.ndarray:
        """
        Generates the baseline shift for the signal using a sinusoidal function.

        Returns
        -------
        baseline : numpy.ndarray
            The baseline shift over time (in volts).

        Equation
        --------
        The baseline shift is modeled as a sinusoidal function:

            baseline(t) = A * sin(ω * t)

        where:
        - A is the amplitude (`self.baseline_shift`).
        - ω is the angular frequency (0.5 * π).
        - t is the time.
        """
        return self.baseline_shift.magnitude * np.sin(0.5 * np.pi * self.time.magnitude) * ureg.volt

    def _generate_pulse_parameters(self) -> tuple:
        """
        Generates random parameters for a Gaussian pulse, including the center, heights for FSC and SSC,
        and the width of the pulse.

        TODO: put real equation here instead of statistical properties.

        Returns
        -------
        center : float
            The center of the pulse in time.
        fsc_height : Quantity
            The height of the pulse in the FSC channel (in volts).
        ssc_height : Quantity
            The height of the pulse in the SSC channel (in volts).
        width : float
            The width of the pulse (standard deviation of the Gaussian).
        """
        width_factor = 10

        center = np.random.uniform(0, self.total_time.magnitude)
        fsc_height = np.random.uniform(100, 1000) * ureg.volt
        ssc_height = np.random.uniform(50, 500) * ureg.volt
        width = np.random.uniform(0.05, 0.2) / width_factor
        return center, fsc_height, ssc_height, width

    def _accumulate_pulse_signal(self, fsc_pulse: GaussianPulse, ssc_pulse: GaussianPulse) -> None:
        """
        Adds the generated pulses to the raw signal arrays for FSC and SSC channels.

        Parameters
        ----------
        fsc_pulse : GaussianPulse
            The Gaussian pulse object for the FSC channel.
        ssc_pulse : GaussianPulse
            The Gaussian pulse object for the SSC channel.

        Notes
        -----
        The pulses are accumulated over the existing signal.
        """
        self.fsc_raw_signal += fsc_pulse.generate(self.time.magnitude)
        self.ssc_raw_signal += ssc_pulse.generate(self.time.magnitude)

    def _add_noise_and_baseline(self, baseline: np.ndarray) -> None:
        """
        Adds Gaussian noise and the baseline shift to the raw signals.

        Parameters
        ----------
        baseline : numpy.ndarray
            The baseline shift to be added to the signals (in volts).
        """
        noise_fsc = (self.noise_level * np.random.normal(size=self.time_points)).to('volt')
        noise_ssc = (self.noise_level * np.random.normal(size=self.time_points)).to('volt')

        self.fsc_raw_signal += baseline + noise_fsc
        self.ssc_raw_signal += baseline + noise_ssc

    def _apply_saturation(self) -> None:
        """
        Applies saturation to the raw signals, ensuring that no values exceed the saturation level.
        """
        self.fsc_raw_signal = np.clip(self.fsc_raw_signal.magnitude, 0, self.saturation_level.magnitude) * ureg.volt
        self.ssc_raw_signal = np.clip(self.ssc_raw_signal.magnitude, 0, self.saturation_level.magnitude) * ureg.volt

    def _discretize_signals(self) -> None:
        """
        Discretizes the FSC and SSC signals into a specified number of bins.

        Notes
        -----
        The discretization process maps continuous signal values into discrete bins.
        """
        self.fsc_raw_signal = self._discretize_signal(self.fsc_raw_signal) * ureg.volt
        self.ssc_raw_signal = self._discretize_signal(self.ssc_raw_signal) * ureg.volt

    def _discretize_signal(self, signal: np.ndarray) -> np.ndarray:
        """
        Discretizes the signal into a specified number of bins.

        Parameters
        ----------
        signal : numpy.ndarray
            The continuous signal to be discretized.

        Returns
        -------
        numpy.ndarray
            The discretized signal.
        """
        bins = np.linspace(np.min(signal.magnitude), np.max(signal.magnitude), self.n_bins)
        digitized = np.digitize(signal.magnitude, bins) - 1
        return bins[digitized]

    def print_properties(self) -> None:
        """
        Prints the key properties of the FlowCytometer in a tabular format using the tabulate library.
        """
        # Prepare the data as a list of key-value pairs
        properties = [
            ["Particle Density", f"{self.particle_density:.2f~#P}"],
            ["Flow Speed", f"{self.flow_speed:.2f~#P}"],
            ["Total Simulation Time", f"{self.total_time:.2f~#P}"],
            ["Acquisition Frequency", f"{self.acquisition_frequency:.2f~#P}"],
            ["Number of Time Points", self.time_points],
            ["Noise Level", f"{self.noise_level}"],
            ["Baseline Shift Amplitude", f"{self.baseline_shift}"],
            ["Saturation Level", f"{self.saturation_level}"],
            ["Number of Discretization Bins", self.n_bins],
            ["Random Seed", self.seed if self.seed is not None else "Not set"],
            ["Estimated Number of Events", self.n_events]
        ]

        # Display the table
        print("FlowCytometer Properties")
        print(tabulate(properties, headers=["Property", "Value"], tablefmt="grid"))

    def _add_to_ax(self, ax: plt.Axes, channel: str = "both") -> None:
        """
        Plots either or both FSC and SSC signals based on the channel parameter.

        Parameters
        ----------
        channel : str, optional
            The channel to plot. Can be "fsc", "ssc", or "both" (default is "both").
        """
        ax.set(
            title='Simulated raw flow-cytometry signal',
            xlabel='Time [seconds]',
            ylabel='Signal Intensity [V]'
        )

        if channel.lower() in ["fsc", "both"]:
            ax.plot(self.time.magnitude, self.fsc_raw_signal.magnitude, color='blue', label='FSC Signal')

        if channel.lower() in ["ssc", "both"]:
            ax.plot(self.time.magnitude, self.ssc_raw_signal.magnitude, color='green', label='SSC Signal')

        ax.legend()


    def plot(self, channel: str = "both") -> None:
        """
        Plots either or both FSC and SSC signals based on the channel parameter.

        Parameters
        ----------
        channel : str, optional
            The channel to plot. Can be "fsc", "ssc", or "both" (default is "both").
        """
        logging.info(f"Plotting the signal for channel: {channel}")

        with plt.style.context(mps):
            figure, ax = plt.subplots(2, 1, figsize=(10, 6))

            self._add_to_ax(ax=ax[0], channel=channel)

            self.scatterer_distribution._add_to_ax(ax=ax[1])

            plt.show()