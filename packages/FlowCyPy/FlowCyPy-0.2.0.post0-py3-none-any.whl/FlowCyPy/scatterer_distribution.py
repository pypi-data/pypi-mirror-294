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
    A class to define and analyze the size and position distribution of scatterers (particles) passing through a flow cytometer.

    Attributes
    ----------
    refractive_index: float
        The refractive index of the particles.
    mean_size : float
        The mean size of the scatterers in meters.
    std_size : float
        The standard deviation of the scatterer size in meters.
    distribution_type : str
        The type of distribution to use for particle size (e.g., 'normal', 'lognormal', 'uniform').
    coupling_factor : str
        The type of coupling factor to generate ('rayleigh', 'uniform').
    """

    flow: object
    refractive_index: float  # Refractive index of the particles
    mean_size: Optional[float] = 1e-6  # Mean size in meters (1 µm)
    std_size: Optional[float] = 0.2e-6  # Standard deviation in meters (0.2 µm)
    distribution_type: Optional[str] = 'normal'  # Size distribution type: 'normal', 'lognormal', 'uniform'
    coupling_factor: Optional[str] = 'rayleigh'  # Coupling factor type: 'rayleigh', 'uniform'

    def __post_init__(self) -> None:
        """Initializes the scatterer distribution and converts size parameters to physical units."""
        self.mean_size *= ureg.meter
        self.std_size *= ureg.meter
        self.sizes = None  # Placeholder for generated sizes

        self.initalize_samples(self.flow.n_events)

    def initalize_samples(self, n_samples: int) -> None:
        """
        Generates random scatterer sizes based on the selected distribution.

        Parameters
        ----------
        n_samples : int
            The number of particle sizes to generate.
        """
        if n_samples <= 0:
            raise ValueError("The number of samples must be greater than 0.")

        n_samples = n_samples.magnitude
        # Use a single match statement to handle all distribution types
        match self.distribution_type.lower():
            case dist if dist.startswith('singular:'):
                size_value = float(dist.split(':')[1])
                sizes = np.full(n_samples, size_value)
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
                raise ValueError(f"Invalid distribution type [{self.distribution_type}]. Choose 'normal', 'lognormal', 'uniform', or 'singular:value'.")

        self.sizes = sizes * ureg.meter

        self.flow._generate_longitudinal_positions(n_samples)

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
            raise ValueError("Sizes have not been generated. Use 'initalize_samples()' first.")

        # Generate x-values for the PDF
        x = np.linspace(self.sizes.magnitude.min(), self.sizes.magnitude.max(), sampling)

        # Match case statement to handle different distribution types
        match self.distribution_type.lower():
            case dist if dist.startswith('singular:'):
                # In the case of a singular value, create a "spike" at the singular size
                singular_value = float(dist.split(':')[1])
                pdf = np.zeros_like(x)
                idx = (np.abs(x - singular_value)).argmin()  # Find the closest x to the singular value
                pdf[idx] = 1.0  # Assign all the probability to this value
            case 'normal':
                pdf = norm.pdf(x, loc=self.mean_size.magnitude, scale=self.std_size.magnitude)
            case 'lognormal':
                pdf = lognorm.pdf(x, s=self.std_size.magnitude, scale=self.mean_size.magnitude)
            case 'uniform':
                pdf = uniform.pdf(x, loc=self.mean_size.magnitude - self.std_size.magnitude, scale=2 * self.std_size.magnitude)
            case _:
                raise ValueError("Invalid distribution type. Choose 'normal', 'lognormal', 'uniform', or 'singular:value'.")

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
            raise ValueError("Scatterer sizes have not been generated. Use 'initalize_samples()' first.")

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
        """Displays the core properties of the scatterer distribution and flow cytometer setup using the `tabulate` library."""

        print("\nScatterers Properties")
        self.flow.print_properties()

        properties = [
            ["Mean size", f"{self.mean_size:.2f~#P}"],
            ["Size standard deviation", f"{self.std_size:.2f~#P}"],
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
            fig, axes = plt.subplots(2, 1, figsize=(8, 2*3))
            self._add_to_ax(ax=axes[0], bins=bins)
            self._add_position_distribution_to_ax(ax=axes[1])
            plt.show()

    def _add_position_distribution_to_ax(self, ax: plt.Axes) -> None:
        """
        Plots the longitudinal positions of scatterers if they have been generated.

        The plot will show the position of particles along the flow tube's longitudinal axis.
        """
        # Create a scatter plot with longitudinal positions
        ax.scatter(
            self.flow.longitudinal_positions.magnitude,
            np.zeros_like(self.flow.longitudinal_positions),
            c='blue',
            marker='|',
            s=100,
            label='Particles'
        )

        ax.set(
            xlabel="Longitudinal Position [m]",
            title="Longitudinal Positions of Scatterers in the Flow Tube",
            yticks=[]
        )