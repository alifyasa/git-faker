from typing import Callable

import numpy as np
import matplotlib.pyplot as plt
from git_commit_sampler.simulation.constants import HOUR

def plot_func(
        func: Callable[[float], float], start = 0.0, end = 100.0, N = 10,
        plot_name="plot", x_step = None, y_step = None,
        width: float = 8, height: float = 6,
    ):
    x = np.linspace(start, end, num=N)
    y = func(x)

    # Plotting
    plt.figure(figsize=(width, height))  # Optional: Adjust the figure size
    plt.plot(x, y, label='y = f(x)')  # Plot x vs. y
    plt.title(f'{plot_name} Plot')  # Optional: Add a title
    plt.xlabel('x')  # Optional: Label the x-axis
    plt.ylabel('y')  # Optional: Label the y-axis
    plt.legend()  # Optional: Add a legend
    plt.grid(True)  # Optional: Show grid

    if x_step != None:
        plt.xticks(
            ticks = np.arange(np.min(x), np.max(x) + 1, x_step),
            labels = (np.arange(np.min(x), np.max(x) + 1, x_step) / x_step).astype(np.integer)
        )
    if y_step != None:
        plt.yticks(
            ticks = np.arange(np.min(y), np.max(y) + 1, y_step),
            labels = (np.arange(np.min(y), np.max(y) + 1, y_step) / y_step).astype(np.integer)
        )

    # Save the plot to a file
    plt.savefig(f"output/plots/{plot_name}.png")
