
import numpy as np
from FlowCyPy import ScattererDistribution, Detector, Source

def compute_rayleigh_scattering_cross_section(scatterer_distribution: ScattererDistribution, source: Source) -> np.ndarray:
    r"""
    Computes the Rayleigh scattering cross-section for a spherical particle.

    The Rayleigh scattering cross-section is given by the formula:

    .. math::
        \sigma_s = \frac{8 \pi}{3} \left( \frac{2 \pi}{\lambda} \right)^4 \left( \frac{n^2 - 1}{n^2 + 2} \right)^2 r^6

    Where:
    - :math:`\sigma_s` is the scattering cross-section (in m²).
    - :math:`r` is the radius of the particle (in m).
    - :math:`\lambda` is the wavelength of the incident light (in m).
    - :math:`n` is the refractive index of the scatterer (dimensionless).

    Parameters
    ----------
    scatterer_distribution : ScattererDistribution
        An instance of `ScattererDistribution` containing the scatterer properties such as size and refractive index.
    source : Source
        An instance of `Source` containing the laser properties, including the wavelength.

    Returns
    -------
    np.ndarray
        The Rayleigh scattering cross-section (in square meters, m²).
    """
    # Extract properties
    refractive_index = scatterer_distribution.refractive_index
    sizes = scatterer_distribution.sizes
    wavelength = source.wavelength

    # Rayleigh scattering cross-section formula components
    factor_0 = 8 * np.pi / 3
    factor_1 = (2 * np.pi / wavelength) ** 4
    factor_2 = ((refractive_index ** 2 - 1) / (refractive_index ** 2 + 2)) ** 2

    # Compute scattering cross-section based on the mean size of scatterers (assuming size in meters)
    cross_section = factor_0 * factor_1 * factor_2 * sizes ** 6

    return cross_section


def compute_detected_signal(source: Source, detector: Detector, scatterer_distribution: ScattererDistribution) -> float:
    r"""
    Computes the power detected by a detector from a Rayleigh scattering event.

    The power scattered by a particle is proportional to the power density of the incident light
    and the scattering cross-section of the particle:

    .. math::
        P_s = I_{\text{incident}} \cdot \sigma_s

    The power detected by the detector depends on the solid angle subtended by the detector
    and the total solid angle over which the power is scattered (assumed to be \( 4\pi \) steradians):

    .. math::
        P_{\text{detected}} = P_s \cdot \frac{\Omega}{4 \pi} \cdot \eta

    Where:
    - :math:`P_{\text{detected}}` is the power detected by the detector (in watts, W).
    - :math:`\Omega` is the solid angle subtended by the detector (in steradians, sr).
    - :math:`\eta` is the detector efficiency (dimensionless, between 0 and 1).

    Parameters
    ----------
    source : Source
        An instance of `Source` containing the laser properties, including the optical power and numerical aperture.
    detector : Detector
        An instance of `Detector` containing the detector properties, including numerical aperture and responsitivity.

    Returns
    -------
    float
        The power detected by the detector (in watts, W).
    """
    scattering_cross_section = compute_rayleigh_scattering_cross_section(
        source=source,
        scatterer_distribution=scatterer_distribution
    )

    # Calculate incident power density at the beam waist
    incident_power_density = (2 * source.optical_power) / (np.pi * source.waist ** 2)

    # Calculate the scattered power using the scattering cross-section
    scattered_power = incident_power_density * scattering_cross_section

    # Detector captures a portion of scattered power proportional to its solid angle over 4π steradians
    solid_angle = detector.numerical_aperture ** 2
    detected_power = scattered_power * (solid_angle / (4 * np.pi))

    # Adjust for detector responsitivity (efficiency)
    detected_power *= detector.responsitivity

    return detected_power