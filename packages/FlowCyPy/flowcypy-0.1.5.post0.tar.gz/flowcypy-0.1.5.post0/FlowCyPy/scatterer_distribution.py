import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, lognorm, uniform
from MPSPlots.styles import mps
from dataclasses import dataclass, field
from pint import UnitRegistry

# Initialize a unit registry
ureg = UnitRegistry()

@dataclass
class ScattererDistribution:
    """
    A class to define the size distribution of scatterers (particles) passing through the flow cytometer.

    Attributes
    ----------
    mean_size : Quantity
        The mean size of the scatterers (in micrometers).
    std_size : Quantity
        The standard deviation of the scatterer size (in micrometers).
    distribution_type : str
        The type of distribution to use (e.g., 'normal', 'lognormal', 'uniform').
    """

    mean_size: float = 1e-6  # meters
    std_size: float = 0.2e-6  # meters
    distribution_type: str = 'normal'  # Distribution type: 'normal', 'lognormal', 'uniform'

    def __post_init__(self) -> None:
        self.mean_size *= ureg.meter
        self.std_size *= ureg.meter
        self.sizes = None

    def generate_size(self, n_samples: int) -> np.ndarray:
        """
        Generates random scatterer sizes based on the selected distribution.

        Parameters
        ----------
        n_samples : int
            The number of particle sizes to generate.

        Returns
        -------
        np.ndarray
            An array of scatterer sizes.
        """
        match self.distribution_type.lower():
            case 'normal':
                sizes = np.random.normal(self.mean_size.magnitude, self.std_size.magnitude, n_samples)
            case 'lognormal':
                sizes = np.random.lognormal(np.log(self.mean_size.magnitude), self.std_size.magnitude, n_samples)
            case 'uniform':
                sizes = np.random.uniform(
                    self.mean_size.magnitude - self.std_size.magnitude,
                    self.mean_size.magnitude + self.std_size.magnitude,
                    n_samples
                )
            case _:
                raise ValueError("Invalid distribution type. Choose 'normal', 'lognormal', or 'uniform'.")

        self.sizes = sizes * ureg.meter

        return self.sizes

    def _plot_continuous_distribution(self, ax: plt.Axes) -> None:
        """
        Plots the continuous distribution curve for the selected distribution type.

        Parameters
        ----------
        ax : plt.Axes
            Matplotlib axis where the continuous distribution will be plotted.
        """
        # Generate a range of values to plot the continuous distribution
        x = np.linspace(self.sizes.magnitude.min(), self.sizes.magnitude.max(), 1000)

        if self.distribution_type.lower() == 'normal':
            pdf = norm.pdf(x, loc=self.mean_size.magnitude, scale=self.std_size.magnitude)
        elif self.distribution_type.lower() == 'lognormal':
            pdf = lognorm.pdf(x, s=self.std_size.magnitude, scale=self.mean_size.magnitude)
        elif self.distribution_type.lower() == 'uniform':
            pdf = uniform.pdf(x, loc=self.mean_size.magnitude - self.std_size.magnitude, scale=2 * self.std_size.magnitude)
        else:
            raise ValueError("Invalid distribution type. Choose 'normal', 'lognormal', or 'uniform'.")

        # Normalize the PDF to the histogram
        ax_ = ax.twinx()
        ax_.plot(x * 1e6, pdf * len(self.sizes) * (x[1] - x[0]), color='red', lw=2)
        ax_.axis('off')

    def _add_to_ax(self, ax: plt.Axes, bins: int = 50) -> None:
        """
        Plots the histogram of scatterer sizes and overlays the continuous distribution.

        Parameters
        ----------
        bins : int, optional
            The number of bins to use in the histogram (default is 50).
        """
        if self.sizes is None:
            raise ValueError(f'Scatterer distribution has not been initialized, use .generate_size() method before plotting.')

        # Convert sizes to micrometers for plotting
        sizes_in_micrometers = self.sizes.to('micrometer').magnitude

        # Plot histogram
        ax.hist(sizes_in_micrometers, bins=bins, edgecolor='black', alpha=0.7, label='Sampled Data')

        # Plot the continuous distribution on top of the histogram
        self._plot_continuous_distribution(ax)

        ax.set(
            title=f'Size Distribution of Scatterers ({self.distribution_type.capitalize()} Distribution)',
            xlabel='Size [micrometers]',
            ylabel='Frequency'
        )
        ax.legend()

    def plot(self, bins: int = 50) -> None:
        """
        Plots the histogram of scatterer sizes and overlays the continuous distribution.

        Parameters
        ----------
        bins : int, optional
            The number of bins to use in the histogram (default is 50).
        """
        with plt.style.context(mps):
            fig, ax = plt.subplots(1, 1, figsize=(8, 5))
            self._add_to_ax(ax=ax, bins=bins)
            plt.show()
