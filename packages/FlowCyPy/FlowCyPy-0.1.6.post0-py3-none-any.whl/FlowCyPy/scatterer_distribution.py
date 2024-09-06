from typing import Tuple, Optional
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, lognorm, uniform
from MPSPlots.styles import mps
from dataclasses import dataclass
from FlowCyPy import ureg
from tabulate import tabulate

@dataclass
class ScattererDistribution:
    """
    A class to define and analyze the size distribution of scatterers (particles) passing through a flow cytometer.

    Attributes
    ----------
    particle_density : float
        The density of particles in the flow (particles per cubic meter).
    mean_size : float
        The mean size of the scatterers in meters.
    std_size : float
        The standard deviation of the scatterer size in meters.
    distribution_type : str
        The type of distribution to use (e.g., 'normal', 'lognormal', 'uniform').
    coupling_factor : str
        The type of coupling factor to generate ('rayleigh', 'uniform').
    """

    particle_density: float  # Density of the particle suspension (#/m^3)
    mean_size: Optional[float] = 1e-6  # Mean size in meters (1 µm)
    std_size: Optional[float] = 0.2e-6  # Standard deviation in meters (0.2 µm)
    distribution_type: Optional[str] = 'normal'  # Distribution type: 'normal', 'lognormal', 'uniform'
    coupling_factor: Optional[str] = 'rayleigh'  # Coupling factor type: 'rayleigh', 'uniform'

    def __post_init__(self) -> None:
        """Initializes the scatterer distribution and converts size parameters to physical units."""
        self.particle_density *= ureg('particles/meter**3')
        self.mean_size *= ureg.meter
        self.std_size *= ureg.meter
        self.sizes = None  # Placeholder for generated sizes
        self.size_coupling_factor = None  # Placeholder for generated coupling factors

    def generate_size(self, n_samples: int) -> None:
        """
        Generates random scatterer sizes based on the selected distribution.

        Parameters
        ----------
        n_samples : int
            The number of particle sizes to generate.
        """
        if n_samples <= 0:
            raise ValueError("The number of samples must be greater than 0.")

        # Generate sizes based on the selected distribution type
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
        self._generate_coupling_factors()

    def _generate_coupling_factors(self) -> None:
        """
        Generates coupling factors for the scatterer sizes based on the selected coupling model.
        """
        if self.sizes is None:
            raise ValueError("Sizes have not been generated. Use 'generate_size()' first.")

        match self.coupling_factor.lower():
            case 'rayleigh':
                self.size_coupling_factor = self.sizes.magnitude ** 6  # Rayleigh scattering (size^6)
            case 'uniform':
                self.size_coupling_factor = np.ones(self.sizes.shape)  # Uniform coupling factor
            case _:
                raise ValueError("Invalid coupling factor type. Choose 'rayleigh' or 'uniform'.")

    def get_pdf(self, sampling: Optional[int] = 1000) -> Tuple[np.ndarray, np.ndarray]:
        """
        Returns the x-values and probability density function (PDF) for the size distribution.

        Parameters
        ----------
        sampling : int, optional
            Number of points to sample for plotting the continuous PDF (default is 1000).

        Returns
        -------
        x : np.ndarray
            The x-values (size) for the PDF.
        pdf : np.ndarray
            The PDF values corresponding to the x-values.
        """
        if self.sizes is None:
            raise ValueError("Sizes have not been generated. Use 'generate_size()' first.")

        # Generate x-values for the PDF
        x = np.linspace(self.sizes.magnitude.min(), self.sizes.magnitude.max(), sampling)

        # Compute the PDF based on the selected distribution
        match self.distribution_type.lower():
            case 'normal':
                pdf = norm.pdf(x, loc=self.mean_size.magnitude, scale=self.std_size.magnitude)
            case 'lognormal':
                pdf = lognorm.pdf(x, s=self.std_size.magnitude, scale=self.mean_size.magnitude)
            case 'uniform':
                pdf = uniform.pdf(x, loc=self.mean_size.magnitude - self.std_size.magnitude, scale=2 * self.std_size.magnitude)
            case _:
                raise ValueError("Invalid distribution type. Choose 'normal', 'lognormal', or 'uniform'.")

        return x, pdf

    def _add_to_ax(self, ax: plt.Axes, bins: Optional[int] = 50) -> None:
        """
        Plots the histogram of scatterer sizes and overlays the probability density function (PDF)
        behind the histogram.

        Parameters
        ----------
        ax : plt.Axes
            The matplotlib axis where the plot will be drawn.
        bins : int, optional
            The number of bins for the histogram (default is 50).
        """
        if self.sizes is None:
            raise ValueError("Scatterer sizes have not been generated. Use 'generate_size()' first.")

        sizes_in_micrometers = self.sizes.to('micrometer').magnitude

        # Plot the histogram of sampled data
        counts, bin_edges, _ = ax.hist(
            sizes_in_micrometers,
            bins=bins,
            edgecolor='black',
            alpha=0.7,
            label='Sampled Data'
        )

        # Plot the continuous PDF behind the histogram
        x_pdf, pdf = self.get_pdf()
        bin_width = bin_edges[1] - bin_edges[0]
        pdf_scaled = pdf * len(sizes_in_micrometers) * bin_width

        ax_ = ax.twinx()
        ax_.plot(x_pdf * 1e6, pdf_scaled, color='red', lw=2, label='PDF', zorder=0)  # PDF plotted behind
        ax_.axis('off')

        # Set labels and legend
        ax.set(
            title=f'Size Distribution of Scatterers ({self.distribution_type.capitalize()} Distribution)',
            xlabel='Size [micrometers]',
            ylabel='Frequency'
        )
        ax.legend()

    def print_properties(self) -> None:
        """Displays the core properties of the flow cytometer and its detectors using the `tabulate` library."""
        properties = [
            ["Particle Density", f"{self.particle_density:.2f~#P}"],
            ["Mean size", f"{self.mean_size:.2f~#P}"],
            ["Size standard deviation", f"{self.std_size:.2f~#P}"],
            ["Size coupling power mechanism", f"{self.coupling_factor}"],
        ]

        print("\nScatterers Properties")
        print(tabulate(properties, headers=["Property", "Value"], tablefmt="grid"))

    def plot(self, bins: Optional[int] = 50) -> None:
        """
        Plots the histogram of scatterer sizes and overlays the continuous probability density function (PDF).

        Parameters
        ----------
        bins : int, optional
            The number of bins for the histogram (default is 50).
        """
        with plt.style.context(mps):
            fig, ax = plt.subplots(1, 1, figsize=(8, 5))
            self._add_to_ax(ax=ax, bins=bins)
            plt.show()
