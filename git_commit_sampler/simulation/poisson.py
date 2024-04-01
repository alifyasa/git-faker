import numpy as np

import cProfile
import pstats

import scipy.stats
import scipy.integrate
import scipy.optimize

from datetime import datetime

from git_commit_sampler.simulation.plot import plot_func
from git_commit_sampler.simulation.constants import MINUTE, HOUR, DAY

def generate_poisson_functions(T: float, start_timestamp: int = 0):

    SAMPLING_RATE = T * 1 // MINUTE # SAMPLING sample per hour
    # Peak hours in the day is at 10, 15:30, and 20:30
    dist_morning = scipy.stats.norm(10 * HOUR, 1 * HOUR)
    dist_afternoon = scipy.stats.norm(15.5 * HOUR, 1 * HOUR)
    dist_evening = scipy.stats.norm(20.5 * HOUR, 1 * HOUR)

    def commit_intensity(t: np.ndarray):
        return (
            # Different weight for each peak hour
            6 * dist_morning.pdf(t % DAY) + # means expected 3 commit in the morning, etc.
            8 * dist_afternoon.pdf(t % DAY) +
            3 * dist_evening.pdf(t % DAY)
        )
    
    ci_X = np.linspace(0, T, num=SAMPLING_RATE)
    ci_Y = commit_intensity(ci_X)
    ci_total = scipy.integrate.simpson(x=ci_X, y=ci_Y)
    
    def lambda_(t: np.ndarray):
        return np.interp(t, ci_X, ci_Y)

    def __single_generate_expectation(t: float):
        x = np.linspace(0, t, num=SAMPLING_RATE)
        y = lambda_(x)
        return scipy.integrate.simpson(x=x, y=y)


    def generate_expectation(t: np.ndarray):
        return np.vectorize(__single_generate_expectation)(t)

    # Both will just use interpolation for speed
    expectation_X = np.linspace(0, T, num=SAMPLING_RATE)
    expectation_Y = generate_expectation(expectation_X)

    def expectation(t: np.ndarray):
        # Integrate lambda_ from 0 to t

        # Is also used as inter-arrival time
        return np.interp(t, expectation_X, expectation_Y)

    def inv_expectation(t: np.ndarray):
        # Inverse of expectation
        return np.interp(t, expectation_Y, expectation_X)

    return (lambda_, expectation, inv_expectation, ci_total)

if __name__ == "__main__":
    with open(f"output/stats/poisson_{int(datetime.now().timestamp())}.txt", "w") as f:
        with cProfile.Profile() as pr:

            T = 3 * DAY
            SAMPLING_RATE = T * 1 // MINUTE

            l, m, t, expected_count = generate_poisson_functions(T)
            plot_func(l, 0, T, SAMPLING_RATE, "Lambda", x_step=HOUR, width= T // (3 * HOUR))
            plot_func(m, 0, T, SAMPLING_RATE, "Expectation", x_step=HOUR, width= T // (3 * HOUR))
            plot_func(
                t, 0, expected_count, SAMPLING_RATE, "Inverse Expectation", y_step= HOUR,
                width= expected_count // 2, height= T // (3 * HOUR)
            )

            ps = pstats.Stats(pr, stream=f)
            ps.sort_stats('cumtime')
            ps.print_stats()