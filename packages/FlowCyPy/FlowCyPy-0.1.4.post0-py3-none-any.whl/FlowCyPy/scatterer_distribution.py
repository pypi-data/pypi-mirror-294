import numpy as np
import matplotlib.pyplot as plt
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

        return sizes * ureg.meter

    def plot(self, n_samples: int = 1000, bins: int = 50) -> None:
        """
        Plots the histogram of scatterer sizes based on the selected distribution.

        Parameters
        ----------
        n_samples : int, optional
            The number of particle sizes to generate (default is 1000).
        bins : int, optional
            The number of bins to use in the histogram (default is 50).
        """
        with plt.style.context(mps):
            sizes = self.generate_size(n_samples)

            # Convert sizes to micrometers for plotting
            sizes_in_micrometers = sizes.to('micrometer').magnitude

            # Plot histogram of the sizes
            plt.figure(figsize=(8, 5))
            plt.hist(sizes_in_micrometers, bins=bins, edgecolor='black', alpha=0.7)

            plt.title(f'Size Distribution of Scatterers ({self.distribution_type.capitalize()} Distribution)')
            plt.xlabel('Size [meters]')
            plt.ylabel('Frequency')
            plt.grid(True)
            plt.show()
