"""
Plotting Utilities
"""

from typing import Callable, Optional
import numpy as np
import matplotlib.pyplot as plt


def plot_func(
    func: Callable[[np.ndarray], np.ndarray],
    start: float = 0.0,
    end: float = 100.0,
    sampling_rate: int = 10,
    options: Optional[dict] = None
):
    """
    Plot a function
    """

    if options is None:
        options = {}

    x = np.linspace(start, end, num=sampling_rate)
    y = func(x)

    plt.figure(figsize=(options.get('width', 8), options.get('height', 6)))
    plt.plot(x, y, label=options.get('label', 'y = f(x)'))
    plt.title(options.get('title', 'Plot'))
    plt.xlabel(options.get('xlabel', 'x'))
    plt.ylabel(options.get('ylabel', 'y'))
    if options.get('legend', False):
        plt.legend()
    plt.grid(options.get('grid', True))

    if 'x_step' in options and 'y_step' in options:
        x_step = options['x_step']
        y_step = options['y_step']
        plt.xticks(
            np.arange(
                np.min(x),
                np.max(x) +
                1,
                x_step),
            (np.arange(
                np.min(x),
                np.max(x) +
                1,
                x_step) /
                x_step).astype(
                np.integer))
        plt.yticks(
            np.arange(
                np.min(y),
                np.max(y) +
                1,
                y_step),
            (np.arange(
                np.min(y),
                np.max(y) +
                1,
                y_step) /
                y_step).astype(
                np.integer))

    # Save the plot to a file
    plt.savefig(f"output/plots/{options.get('plot_name', 'plot')}.png")
