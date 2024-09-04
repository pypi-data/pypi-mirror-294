

import numpy as np
import matplotlib.pyplot as plt
from MPSPlots.styles import mps
from dataclasses import dataclass, field
from pint import UnitRegistry
from FlowCyPy.gaussian_pulse import GaussianPulse

# Initialize a unit registry
ureg = UnitRegistry()

@dataclass
class FlowCytometer:
    """
    A dataclass to simulate the operation of a flow cytometer, generating realistic raw signals
    for Forward Scatter (FSC) and Side Scatter (SSC)  channels.

    Attributes
    ----------
    particle_density : Quantity
        The density of particles in the flow (particles per cubic meter).
    flow_speed : Quantity
        The speed of the flow (meters per second).
    acquisition_frequency : Quantity
        The frequency at which the data is sampled (in Hertz).
    noise_level : float
        The level of noise added to the signal (as a fraction of the signal amplitude).
    baseline_shift : float
        The amplitude of the baseline shift added to the signal.
    saturation_level : float
        The maximum signal level before saturation occurs.
    n_bins : int
        The number of bins to discretize the signal into.
    time : numpy.ndarray
        A numpy array representing the time axis for the simulation (in seconds).
    fsc_raw_signal : numpy.ndarray
        The simulated raw signal for the FSC channel.
    ssc_raw_signal : numpy.ndarray
        The simulated raw signal for the SSC channel.
    """

    particle_density: float  # particles per cubic meter
    flow_area: float # Area of the flow of particle
    flow_speed: float  # meters per second
    total_time: float  # seconds
    acquisition_frequency: float  # Hertz
    noise_level: float = 0.05
    baseline_shift: float = 0.01
    saturation_level: float = 1e3
    n_bins: int = 100
    time: np.ndarray = field(init=False)
    fsc_raw_signal: np.ndarray = field(init=False)
    ssc_raw_signal: np.ndarray = field(init=False)
    seed: int = 42

    def __post_init__(self) -> None:
        """Initializes fields that depend on other fields."""
        self.particle_density *= ureg('particles/meter**3')
        self.flow_speed *= ureg('meter/second')
        self.total_time *= ureg.second
        self.flow_area *= ureg('meter**2')
        self.acquisition_frequency *= ureg.hertz

       # Calculate the number of time points based on the acquisition frequency and total time
        self.time_points = int((self.acquisition_frequency * self.total_time).to('dimensionless').magnitude)

        self.time = np.linspace(0, self.total_time.magnitude, self.time_points) * ureg.second

        self.fsc_raw_signal = np.zeros(self.time_points)
        self.ssc_raw_signal = np.zeros(self.time_points)
        dt = self.total_time.to('second')

        self.rate_of_particle = (self.particle_density * self.flow_speed * self.flow_area)
        self.n_events = self.rate_of_particle * dt  # Estimate the number of events

        np.random.seed(self.seed)

    def simulate_pulse(self) -> None:
        """
        Main function to simulate pulses for FSC and SSC channels.
        This function calls smaller, dedicated methods to handle different parts of the process.
        """
        baseline = self._generate_baseline_shift()

        for _ in range(int(self.n_events.magnitude)):
            center, fsc_height, ssc_height, width = self._generate_pulse_parameters()

            fsc_pulse = GaussianPulse(center, fsc_height, width)
            ssc_pulse = GaussianPulse(center, ssc_height, width)

            self._accumulate_pulse_signal(fsc_pulse, ssc_pulse)

        self._add_noise_and_baseline(baseline)
        self._apply_saturation()
        self._discretize_signals()

    def _generate_baseline_shift(self) -> np.ndarray:
        """
        Generates the baseline shift for the signal using a sinusoidal function.

        Returns
        -------
        baseline : numpy.ndarray
            The baseline shift over time.

        Equation
        --------
        The baseline shift is modeled as a sinusoidal function:

            baseline(t) = A * sin(ω * t)

        where:
        - A is the amplitude (`self.baseline_shift`).
        - ω is the angular frequency (0.5 * π).
        - t is the time.
        """
        return self.baseline_shift * np.sin(0.5 * np.pi * self.time.magnitude)

    def _generate_pulse_parameters(self) -> tuple:
        """
        Generates random parameters for a Gaussian pulse, including the center, heights for FSC and SSC,
        and the width of the pulse.

        Returns
        -------
        center : float
            The center of the pulse in time.
        fsc_height : float
            The height of the pulse in the FSC channel.
        ssc_height : float
            The height of the pulse in the SSC channel.
        width : float
            The width of the pulse (standard deviation of the Gaussian).

        Notes
        -----
        The parameters are generated randomly within specified ranges.
        """
        center = np.random.uniform(0, self.total_time.magnitude)
        fsc_height = np.random.uniform(100, 1000)
        ssc_height = np.random.uniform(50, 500)
        width = np.random.uniform(0.05, 0.2)
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
            The baseline shift to be added to the signals.

        Notes
        -----
        Noise is modeled as a Gaussian distribution added to the signal.
        """
        noise_fsc = self.noise_level * np.random.normal(size=self.time_points)
        noise_ssc = self.noise_level * np.random.normal(size=self.time_points)

        self.fsc_raw_signal += baseline + noise_fsc
        self.ssc_raw_signal += baseline + noise_ssc

    def _apply_saturation(self) -> None:
        """
        Applies saturation to the raw signals, ensuring that no values exceed the saturation level.

        Notes
        -----
        Signal saturation is implemented by clipping the signal values at the maximum allowable level.
        """
        self.fsc_raw_signal = np.clip(self.fsc_raw_signal, 0, self.saturation_level)
        self.ssc_raw_signal = np.clip(self.ssc_raw_signal, 0, self.saturation_level)

    def _discretize_signals(self) -> None:
        """
        Discretizes the FSC and SSC signals into a specified number of bins.

        Notes
        -----
        The discretization process maps continuous signal values into discrete bins.
        """
        self.fsc_raw_signal = self._discretize_signal(self.fsc_raw_signal)
        self.ssc_raw_signal = self._discretize_signal(self.ssc_raw_signal)

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
        bins = np.linspace(np.min(signal), np.max(signal), self.n_bins)
        digitized = np.digitize(signal, bins) - 1
        return bins[digitized]

    def plot(self, channel: str = "both") -> None:
        """
        Plots either or both FSC and SSC signals based on the channel parameter.

        Parameters
        ----------
        channel : str, optional
            The channel to plot. Can be "fsc", "ssc", or "both" (default is "both").
        """
        with plt.style.context(mps):
            figure, ax = plt.subplots(1, 1, figsize=(10, 5))
            ax.set(
                title='Simulated raw flow-cytometry signal',
                xlabel='Time',
                ylabel='Signal Intensity'
            )

            if channel.lower() in ["fsc", "both"]:
                ax.plot(self.time.magnitude, self.fsc_raw_signal, color='blue', label='FSC Signal')

            if channel.lower() in ["ssc", "both"]:
                ax.plot(self.time.magnitude, self.ssc_raw_signal, color='green', label='SSC Signal')

            ax.legend()

            ax.grid(True)
            plt.show()

    def print_properties(self) -> None:
        """
        Prints the key properties of the FlowCytometer.
        """
        print(
            "FlowCytometer Properties:"
            f"\n  Particle Density: {self.particle_density:.2f~#P}"
            f"\n  Flow Speed: {self.flow_speed:.2f~#P}"
            f"\n  Total Simulation Time: {self.total_time:.2f~#P}"
            f"\n  Acquisition frequency: {self.acquisition_frequency:.2f~#P}"
            f"\n  Number of Time Points: {self.time_points}"
            f"\n  Noise Level: {self.noise_level}"
            f"\n  Baseline Shift Amplitude: {self.baseline_shift}"
            f"\n  Saturation Level: {self.saturation_level}"
            f"\n  Number of Discretization Bins: {self.n_bins}"
            f"\n  Random Seed: {self.seed}"
            f"\n  Estimated Number of Events: {self.n_events}"
        )