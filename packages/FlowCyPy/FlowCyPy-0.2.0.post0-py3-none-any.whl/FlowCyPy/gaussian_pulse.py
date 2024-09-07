

from typing import Optional
import numpy as np
import matplotlib.pyplot as plt
from MPSPlots.styles import mps

class GaussianPulse:
    """
    A class to represent a Gaussian pulse used in simulating flow cytometry signals.

    Attributes
    ----------
    center : float
        The center of the Gaussian pulse in time (microseconds).
    height : float
        The peak height (amplitude) of the Gaussian pulse (volts).
    width : float
        The width (standard deviation) of the Gaussian pulse (microseconds).

    Methods
    -------
    generate(time):
        Generates the Gaussian pulse over a given time axis.
    plot(time=None):
        Plots the Gaussian pulse over a given time axis. If no time axis is provided, a default is used.

    Equations
    ---------
    The Gaussian pulse is generated using the equation:

        V(t) = height * exp(-((t - center)^2) / (2 * width^2))

    where:
        - V(t) is the signal amplitude at time t (volts),
        - height is the peak amplitude of the pulse (volts),
        - center is the time at which the pulse is centered (microseconds),
        - width is the standard deviation of the Gaussian function (microseconds).
    """

    def __init__(self, center: float, height: float, width: float) -> None:
        """
        Constructs all the necessary attributes for the GaussianPulse object.

        Parameters
        ----------
        center : float
            The center of the Gaussian pulse in time (microseconds).
        height : float
            The peak height (amplitude) of the Gaussian pulse (volts).
        width : float
            The width (standard deviation) of the Gaussian pulse (microseconds).
        """
        self.center = center
        self.height = height
        self.width = width

    def generate(self, time: np.ndarray) -> np.ndarray:
        """
        Generates the Gaussian pulse over a given time axis.

        Parameters
        ----------
        time : numpy.ndarray
            A numpy array representing the time axis over which the pulse is generated (microseconds).

        Returns
        -------
        numpy.ndarray
            A numpy array representing the generated Gaussian pulse (volts).
        """
        return self.height * np.exp(-((time - self.center) ** 2) / (2 * self.width ** 2))

    def plot(self, time: Optional[np.ndarray] = None) -> None:
        """
        Plots the Gaussian pulse over a given time axis. If no time axis is provided, a default is used.

        Parameters
        ----------
        time : numpy.ndarray, optional
            A numpy array representing the time axis over which the pulse is generated and plotted (microseconds).
            If not provided, a default time axis will be used.
        """
        if time is None:
            time = np.linspace(self.center - 5*self.width, self.center + 5*self.width, 1000)

        pulse = self.generate(time)
        with plt.style.context(mps):
            figure, ax = plt.subplots(1, 1)

            ax.plot(
                time,
                pulse,
                label=f'Center={self.center} μs, Height={self.height} V, Width={self.width} μs'
            )

            ax.set(
                title='Gaussian Pulse',
                xlabel='Time (μs)',
                ylabel='Amplitude (V)'
            )

            plt.legend()

            plt.show()

    def _add_to_ax(self, ax: plt.Axes) -> None:
        """
        Adds the processed signal to a matplotlib Axes for plotting.

        Parameters
        ----------
        ax : plt.Axes
            The matplotlib Axes object where the signal will be plotted.
        color : str, optional
            The color of the plot (default is 'C0').
        """
        ax.vlines(
            x=self.center.magnitude,
            ymin=0,
            ymax=1,
            color='black',
            linewidth=1,
            linestyle='--',
            transform=ax.get_xaxis_transform(),
        )
