"""
Generate functions necessary for NHPP simulation.

Use generate_poisson_functions to generate:
 1. Git Commit Intensity Function
 2. Expected number of commit to time t
 3. Inverse of function number 2.
 4. Total expected number of commits.
"""

import cProfile
import pstats

from typing import Callable
from datetime import datetime

import scipy.stats
import scipy.integrate
import scipy.optimize

import numpy as np
import pandas as pd

from git_faker.simulation.plot import plot_func
from git_faker.simulation.constants import MINUTE, HOUR, DAY, SECOND


def generate_lambda(total_time: int, start_timestamp: float, sampling_rate: int):
    """
    Generate lambda based on commit_intensity. Used interpolation for
    faster computation.
    """
    current_timezone = datetime.now().astimezone().tzinfo 

    # Peak hours in the day is at 10, 15:30, and 20:30
    dist_morning = scipy.stats.norm(9 * HOUR, 2 * HOUR)
    dist_afternoon = scipy.stats.norm(14.5 * HOUR, 1 * HOUR)
    dist_evening = scipy.stats.norm(20.5 * HOUR, 0.5 * HOUR)

    def commit_intensity(t: np.ndarray):
        timestamps = t + start_timestamp

        datetimes = pd.to_datetime(timestamps, unit="s").tz_localize('UTC').tz_convert(current_timezone)

        dt_time = datetimes.hour * HOUR + datetimes.minute * MINUTE + datetimes.second * SECOND
        dt_dayofweek = datetimes.day_of_week
        
        is_weekend = dt_dayofweek >= 5

        # Commit in weekends can be more or less of week days
        #   The rationale is that I have a life (less commit)
        #   But I still code personal projects in weekends (more commit)
        mult_day_of_week = np.where(is_weekend, np.random.uniform(1 / 3, 3), 1)

        # Motivation fluctuates like a sine function
        mult_motivation = (np.sin(timestamps / (3 * DAY) * np.pi) + 2) / 2
        return (
            (
                # Different weight for each peak hour
                # means expected 3 commit in the morning, etc.
                6 * dist_morning.pdf(dt_time % DAY)
                + 8 * dist_afternoon.pdf(dt_time % DAY)
                + 3 * dist_evening.pdf(dt_time % DAY)
            )
            * mult_day_of_week
            * mult_motivation
        )

    ci_x = np.linspace(0, total_time, num=sampling_rate)
    ci_y = commit_intensity(ci_x)
    mean_expectation = scipy.integrate.simpson(x=ci_x, y=ci_y)

    def lambda_(t: np.ndarray):
        return np.interp(t, ci_x, ci_y)

    return lambda_, mean_expectation


def generate_expectation_with_inverse(
    total_time: int, lambda_: Callable[[np.ndarray], np.ndarray], sampling_rate: int
):
    """
    Integrate lambda over some time t. Also returns the inverse function.
    """

    def __single_generate_expectation(t: float):
        x = np.linspace(0, t, num=sampling_rate)
        y = lambda_(x)
        return scipy.integrate.simpson(x=x, y=y)

    def generate_expectation(t: np.ndarray):
        return np.vectorize(__single_generate_expectation)(t)

    # Both will just use interpolation for speed
    expectation_x = np.linspace(0, total_time, num=sampling_rate)
    expectation_y = generate_expectation(expectation_x)

    def expectation(t: np.ndarray):
        # Integrate lambda_ from 0 to t

        # Is also used as inter-arrival time
        return np.interp(t, expectation_x, expectation_y)

    def inv_expectation(t: np.ndarray):
        # Inverse of expectation
        return np.interp(t, expectation_y, expectation_x)

    return expectation, inv_expectation


def generate_poisson_functions(total_time: float, start_timestamp: float = 0):
    """
    Generate:
     1. Lambda (git commit intensity)
     2. Mu (expected number of commit at time t)
     3. Tau (inverse of Mu)
     4. Total expected number of commit = Mu(total_time)
    """

    sampling_rate = total_time // (5 * MINUTE)  # SAMPLING sample per hour

    lambda_, mean_expectation = generate_lambda(
        total_time, start_timestamp, sampling_rate
    )

    expectation, inv_expectation = generate_expectation_with_inverse(
        total_time, lambda_, sampling_rate
    )

    return (lambda_, expectation, inv_expectation, mean_expectation)


if __name__ == "__main__":
    with open(
        f"output/stats/poisson_{int(datetime.now().timestamp())}.txt",
        "w",
        encoding="utf-8",
    ) as f:
        with cProfile.Profile() as pr:

            # Runs linearly with 1 second per day
            start_time = np.floor(datetime.now().timestamp())
            T = 30 * DAY

            lmbd, mu, tau, expected_count = generate_poisson_functions(T, start_time)

            PLOT_SAMPLING_RATE = T // (5 * MINUTE)

            print(expected_count / T * DAY)

            plot_func(
                lmbd,
                0,
                T,
                PLOT_SAMPLING_RATE,
                options={
                    "plot_name": "Lambda",
                    "x_step": HOUR,
                    "width": T // (3 * HOUR),
                },
            )
            plot_func(
                mu,
                0,
                T,
                PLOT_SAMPLING_RATE,
                options={
                    "plot_name": "Expectation",
                    "x_step": HOUR,
                    "width": T // (3 * HOUR),
                },
            )
            plot_func(
                tau,
                0,
                expected_count,
                PLOT_SAMPLING_RATE,
                options={
                    "plot_name": "Inverse Expectation",
                    "y_step": HOUR,
                    "width": expected_count // 2,
                    "height": T // (3 * HOUR),
                },
            )

            ps = pstats.Stats(pr, stream=f)
            ps.sort_stats("cumtime")
            ps.print_stats()
