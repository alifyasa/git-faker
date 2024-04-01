import math
import cProfile
import numpy as np
import matplotlib.pyplot as plt

from typing import Callable
from datetime import datetime, timedelta

from git_commit_sampler.pdf import create_pdf
from git_commit_sampler.sampler import rejection_sample

from scipy.integrate import quad as integrate
from scipy.stats import norm

def plot_func(func: Callable[[float], float], start = 0.0, end = 100.0, N = 10):
    x = np.linspace(start, end, N)
    y = np.vectorize(func)(x)

    # Plotting
    plt.figure(figsize=(8, 6))  # Optional: Adjust the figure size
    plt.plot(x, y, label='y = f(x)')  # Plot x vs. y
    plt.title('Function Plot')  # Optional: Add a title
    plt.xlabel('x')  # Optional: Label the x-axis
    plt.ylabel('y')  # Optional: Label the y-axis
    plt.legend()  # Optional: Add a legend
    plt.grid(True)  # Optional: Show grid

    # Save the plot to a file
    plt.savefig('plot.png')

def main():
    with cProfile.Profile() as pr:
        start_time = datetime.now()
        end_time = start_time + timedelta(days=1)

        unix_start = math.floor(start_time.timestamp())
        unix_end = math.floor(end_time.timestamp())

        T = unix_end - unix_start

        dist = norm(T / 2, 60 * 60)
        def __lambda(t):
            return dist.pdf(t) * 5 / 3600

        pdf = create_pdf(T, __lambda)
        plot_func(pdf, 0, T)
        pr.print_stats('tottime')

if __name__ == "__main__":
    main()