import logging
import numpy as np
from dataclasses import dataclass, field
from pint import UnitRegistry

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize a unit registry
ureg = UnitRegistry()

@dataclass
class SignalProcessor:
    """
    A dataclass to process signals, adding noise, applying saturation, and discretizing signals.

    Attributes
    ----------
    fsc_signal : np.ndarray
        Forward Scatter signal.
    ssc_signal : np.ndarray
        Side Scatter signal.
    noise_level : Quantity
        The noise level to be added to the signal (in volts).
    baseline_shift : Quantity
        The baseline shift to be applied (in volts).
    saturation_level : Quantity
        Maximum signal value before saturation (in volts).
    n_bins : int
        Number of bins for signal discretization.
    time_points : int
        Number of time points for the simulation.
    """
    fsc_signal: np.ndarray
    ssc_signal: np.ndarray
    noise_level: float
    baseline_shift: float
    saturation_level: float
    n_bins: int
    time_points: int

    def add_noise_and_baseline(self, baseline: np.ndarray) -> None:
        """
        Adds Gaussian noise and baseline shift to the signals.

        Parameters
        ----------
        baseline : numpy.ndarray
            The baseline shift to be added (in volts).
        """
        noise_fsc = (self.noise_level * np.random.normal(size=self.time_points)).to('volt')
        noise_ssc = (self.noise_level * np.random.normal(size=self.time_points)).to('volt')

        self.fsc_signal += baseline + noise_fsc
        self.ssc_signal += baseline + noise_ssc

    def apply_saturation(self) -> None:
        """
        Applies saturation to the signals.
        """
        self.fsc_signal = np.clip(self.fsc_signal.magnitude, 0, self.saturation_level.magnitude) * ureg.volt
        self.ssc_signal = np.clip(self.ssc_signal.magnitude, 0, self.saturation_level.magnitude) * ureg.volt

    def discretize_signals(self) -> None:
        """
        Discretizes the FSC and SSC signals into a specified number of bins.
        """
        self.fsc_signal = self._discretize_signal(self.fsc_signal) * ureg.volt
        self.ssc_signal = self._discretize_signal(self.ssc_signal) * ureg.volt

    def _discretize_signal(self, signal: np.ndarray) -> np.ndarray:
        """
        Discretizes a signal into a specified number of bins.

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
