from typing import Callable

import numpy as np
import matplotlib.pyplot as plt

def plot_func(
        func: Callable[[float], float], start = 0.0, end = 100.0, N = 10, 
        plot_name="plot", x_step = 1.0
    ):
    x = np.linspace(start, end, num=N)
    y = func(x)

    # Plotting
    plt.figure(figsize=(8, 8))  # Optional: Adjust the figure size
    plt.plot(x, y, label='y = f(x)')  # Plot x vs. y
    plt.title(f'{plot_name} Plot')  # Optional: Add a title
    plt.xlabel('x')  # Optional: Label the x-axis
    plt.ylabel('y')  # Optional: Label the y-axis
    plt.legend()  # Optional: Add a legend
    plt.grid(True)  # Optional: Show grid

    plt.xticks(
        ticks = np.arange(np.min(x), np.max(x) + 1, x_step),
        labels = (np.arange(np.min(x), np.max(x) + 1, x_step) / x_step).astype(np.integer)
    )

    # Save the plot to a file
    plt.savefig(f"output/plots/{plot_name}.png")
