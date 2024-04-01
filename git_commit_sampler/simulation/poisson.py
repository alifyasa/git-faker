import numpy as np

import cProfile
import pstats

import scipy.stats
import scipy.integrate
import scipy.optimize

from datetime import datetime

from git_commit_sampler.simulation.plot import plot_func
from git_commit_sampler.simulation.constants import HOUR, DAY

SAMPLING = 10_000

def generate_poisson_functions(T: float):

    # Peak hours in the day is at 10, 15:30, and 20:30
    dist_morning = scipy.stats.norm(10 * HOUR, 1 * HOUR)
    dist_afternoon = scipy.stats.norm(15.5 * HOUR, 1 * HOUR)
    dist_evening = scipy.stats.norm(20.5 * HOUR, 1 * HOUR)

    def commit_intensity(t: np.ndarray):
        return (
            # Different weight for each peak hour
            3 * dist_morning.pdf(t % DAY) + # means expected 3 commit in the morning, etc.
            4 * dist_afternoon.pdf(t % DAY) +
            2 * dist_evening.pdf(t % DAY)
        )
    
    ci_X = np.linspace(0, T, num=SAMPLING)
    ci_Y = commit_intensity(ci_X)
    ci_total = scipy.integrate.simpson(x=ci_X, y=ci_Y)
    
    def lambda_(t: np.ndarray):
        return np.interp(t, ci_X, ci_Y) / ci_total

    def generate_expectation(t: np.ndarray):
        x = np.linspace(0, t, num=SAMPLING)
        y = lambda_(x)
        return scipy.integrate.simpson(x=x, y=y)

    # Both will just use interpolation for speed
    expectation_X = np.linspace(0, T, num=SAMPLING)
    expectation_Y = generate_expectation(expectation_X)

    def expectation(t: np.ndarray):
        # Integrate lambda_ from 0 to t

        # Is also used as inter-arrival time
        return np.interp(t, expectation_X, expectation_Y)

    def inv_expectation(t: np.ndarray):
        # Inverse of expectation
        return np.interp(t, expectation_Y, expectation_X)

    return (lambda_, expectation, inv_expectation)

if __name__ == "__main__":
    with open(f"output/stats/poisson_{int(datetime.now().timestamp())}.txt", "w") as f:
        with cProfile.Profile() as pr:

            l, m, t = generate_poisson_functions(3 * DAY)
            plot_func(l, 0, 3 * DAY, SAMPLING, "Lambda", x_step=HOUR)
            plot_func(m, 0, 3 * DAY, SAMPLING, "Expectation", x_step=HOUR)
            plot_func(t, 0, 1, SAMPLING, "Inverse Expectation")

            ps = pstats.Stats(pr, stream=f)
            ps.sort_stats('cumtime')
            ps.print_stats()