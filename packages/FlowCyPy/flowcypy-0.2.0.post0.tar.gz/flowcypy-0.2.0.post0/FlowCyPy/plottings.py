

import matplotlib.pyplot as plt
from MPSPlots.styles import mps

def plot_system(cytometer = None, scatterer_distribution = None, analyzer = None):

    n_figure = bool(cytometer) + bool(scatterer_distribution) + bool(analyzer)

    with plt.style.context(mps):
        figure, axes = plt.subplots(n_figure, 1, figsize=(10, 3 * n_figure))

    for element, ax in zip(elements, axes):
        element._add_to_ax(ax=ax)

    plt.show()